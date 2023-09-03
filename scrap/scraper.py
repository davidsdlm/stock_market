import abc
import json
import datetime
import logging

from .models import News

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

logger = logging.getLogger('main')


class BaseScraper(abc.ABC):
    @abc.abstractmethod
    def __init__(self):
        self.headers = {
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 \
                    (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15',
            'Upgrade-Insecure-Requests': '1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng, \
                    */*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'en-US,en;q=0.9'
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

    def scrap_news(self) -> News:
        try:
            logger.info(f'connect to {self.url}')
            catalogue_html = self.get_html(self.catalogue_url)
            news_url = self.extract_latest_news_url(catalogue_html)
            news_html = self.get_html(news_url)
            news_text = self.extract_text(news_html)
            news_date = str(datetime.datetime.now(datetime.timezone.utc))
            logger.info(f'connect to {self.url} finished')
            return News(news_url, news_text, news_date)
        except Exception as e:
            self.change_headers()
            e.__suppress_context__ = True
            logger.exception("third part scraping error, change request headers",
                             {"args": {"args_func": locals(), "args_class": self.__dict__.copy()}}, exc_info=True)


class BloombergScraper(BaseScraper):
    def __init__(self, url: str, category: str):
        BaseScraper.__init__(self)
        self.url = url
        self.category = category
        self.catalogue_url = self.url + '/' + self.category

    def extract_text(self, html):
        html = BeautifulSoup(html, 'html.parser')
        article_json = html.find_all('script', attrs={'id': "__NEXT_DATA__"})[0].text

        text = ''
        useless = False
        text_key = 'value'

        def _decode_dict(dct):
            nonlocal useless, text
            # values after news-rsf-contact-reporter class are useless, so we add None and to markq
            if (dct.get('title', 0) == 'Read More'
                    or dct.get('class') == "news-rsf-contact-reporter"):
                useless = True

            if dct.get(text_key, 0) and not useless:
                text += " " + dct[text_key]

        json.loads(article_json, object_hook=_decode_dict)

        return text

    def extract_latest_news_url(self, html):
        html = BeautifulSoup(html, 'html.parser')
        latest_news = html.find_all("h3", string='The Latest')[0].findNext('article').findNext('a')
        url_latest_news = self.url + latest_news['href']
        return url_latest_news
