from .scheduler import Scheduler
from .db import DB, DBInfo
from .service import Service
from .models import News
from .repository import insert_news
from .scraper import BaseScraper, BloombergScraper

import logging.config
import json
import datetime
from typing import Any


class CustomLogger(logging.Formatter, logging.Filter):
    def filter(self, record):
        return False

    @staticmethod
    def supress_third_part_loggers():
        third_part_logger = [
            'apscheduler.executors',
            'apscheduler',
            'apscheduler.jobstores',
            'apscheduler.scheduler',
            'apscheduler.executors.default',
            'apscheduler.jobstores.default'
        ]

        for name in third_part_logger:
            logging.getLogger(name).addFilter(CustomLogger())

    def remove_unserializable_keys(self, data: dict[Any]):
        types = [dict, list, set, frozenset, tuple, str, int, float]
        unserializable_keys = []

        for key, value in data.items():
            if isinstance(value, dict):
                self.remove_unserializable_keys(value)
            else:
                if type(value) not in types:
                    unserializable_keys.append(key)
                else:
                    if type(value) is str:
                        if len(value) > 200:
                            unserializable_keys.append(key)

        for index in unserializable_keys:
            data.pop(index)

    def format(self, record):
        # calls logging.Formatter's inherited format method to parse record object attributes (message, args,...)
        # logging.Formatter should stand first not to mess the inheritance tree
        super(CustomLogger, self).format(record)

        if isinstance(record.args, dict):
            self.remove_unserializable_keys(record.args)

        return json.dumps(
            {
                'levelname': record.levelname,
                'time': datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S:%f %z"),
                'message': record.message,
                'exc_info': record.exc_text,
                'args': record.args,
                'pathname': record.pathname,
                'file': record.filename,
                'func': record.funcName,
                'line': record.lineno,
            },
            ensure_ascii=False
        )


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'default': {
            'format': '[%(levelname)s:%(asctime)s] : %(message)s [%(pathname)s, line %(lineno)d, in %(funcName)s]'
        },
        'json': {
            '()': CustomLogger
        }
    },

    'handlers': {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
            "level": "INFO",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "json",
            "level": "INFO",
            "filename": 'log.log',
            "mode": "w",
            "maxBytes": 500000,
            "backupCount": 4
        }
    },

    'loggers': {
        'main': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True
        }
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
# CustomLogger.supress_third_part_loggers()
