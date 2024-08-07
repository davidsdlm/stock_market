import abc
import datetime
import json
import urllib.parse

import backoff
import requests
import structlog
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from app import models

logger = structlog.getLogger("scraper")


class RobotPage(Exception):
    def __init__(self):
        super().__init__("We stuck on robot page")


class BaseScraper(abc.ABC):
    @abc.abstractmethod
    def __init__(self):
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en",
            "Priority": "u=0, i",
            "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": None,
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
        }
        self.url = None
        self.catalogue_url = None
        self.user_agent = UserAgent()

    @abc.abstractmethod
    def extract_text(self, html: str) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def extract_latest_news_url(self, html: str) -> str:
        raise NotImplementedError

    def get_html(self, url: str) -> str:
        req = requests.get(url, headers=self.headers)
        return req.text

    def change_headers(self):
        self.headers['User-Agent'] = self.user_agent.random
        self.headers['Cookie'] = ''

        req = requests.get(self.url, headers=self.headers)
        cookie_string = "; ".join([str(x) + "=" + str(y) for x, y in req.cookies.get_dict().items()])
        self.headers['Cookie'] = cookie_string

    @backoff.on_exception(backoff.expo, RobotPage, on_backoff=lambda details: details['args'][0].change_headers(),
                          max_tries=3)
    def scrap_news(self) -> models.News:
        logger.info(f'connect to {self.catalogue_url}')
        catalogue_html = self.get_html(self.catalogue_url)
        if BeautifulSoup(catalogue_html, 'html.parser').find("meta", attrs={"name": "robots"}):
            raise RobotPage

        logger.info(f'connect to {self.catalogue_url} finished')

        news_url = self.extract_latest_news_url(catalogue_html)

        logger.info(f'connect to {news_url}')
        news_html = self.get_html(news_url)
        logger.info(f'connect to {news_url} finished')

        news_text = self.extract_text(news_html)
        news_date = str(datetime.datetime.now(datetime.timezone.utc))
        return models.News(pk=news_url, content=news_text, date=news_date)


class BloombergScraper(BaseScraper):
    def __init__(self, url: str, category: str):
        BaseScraper.__init__(self)
        self.url = url
        self.category = category
        self.catalogue_url = urllib.parse.urljoin(self.url, self.category)

    def extract_text(self, html: str) -> str:
        html = BeautifulSoup(html, 'html.parser')
        article_json = html.find_all('script', attrs={'id': "__NEXT_DATA__"})[0].text

        text = ''
        useless = False
        text_key = 'value'

        def _decode_dict(dct):
            nonlocal useless, text
            # values after news-rsf-contact-reporter class are useless, so we add None and to markq
            if dct.get('title', 0) == 'Read More' or dct.get('class') == "news-rsf-contact-reporter":
                useless = True

            if dct.get(text_key, 0) and not useless:
                text += " " + dct[text_key]

        json.loads(article_json, object_hook=_decode_dict)

        return text

    def extract_latest_news_url(self, html: str) -> str:
        html = BeautifulSoup(html, 'html.parser')
        latest_news = (html.find('h3', string="Latest")
                       .findNext('div', attrs={'data-component': 'headline'})
                       .findNext('a'))
        url_latest_news = urllib.parse.urljoin(self.url, latest_news['href'])
        return url_latest_news
