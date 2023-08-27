from .scraper import BaseScraper
from .models import News
from .db import DB, DBInfo
from .repository import insert_news
from .scheduler import Scheduler

import logging

logger = logging.getLogger('main')


class Service:
    def __init__(self, scraper: BaseScraper, db_info: DBInfo, interval: float):
        self.scraper = scraper
        self.db: DB = DB(db_info)
        self.scheduler: Scheduler = Scheduler(interval)
        self.latest_news: News = None

    def service(self):
        news = self.scraper.scrap_news()
        if self.latest_news is not None:
            if news.url == self.latest_news.url:
                return

        self.latest_news = news
        insert_news(self.db, news)

    def __enter__(self):
        return self

    def __call__(self, *args, **kwargs):
        logger.info("initialize db")
        self.db.start_up()
        logger.info("initialize scheduler")
        self.scheduler.start_up(self.service)

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.info("shutdown scheduler")
        self.scheduler.shut_down()
        logger.info("shutdown db")
        self.db.shut_down()
