from .scheduler import Scheduler
from .db import DB, DBInfo
from .service import Service
from .models import News
from .repository import insert_news
from .scraper import BaseScraper, BloombergScraper

import logging.config
import json
import datetime


class NoThirdPartFilter(logging.Filter):
    def filter(self, record):
        return False


third_part_logger = [
    'apscheduler.executors',
    'apscheduler',
    'apscheduler.jobstores',
    'apscheduler.scheduler',
    'apscheduler.executors.default',
    'apscheduler.jobstores.default'
]

for name in third_part_logger:
    logging.getLogger(name).addFilter(NoThirdPartFilter())


class JSONFormatter(logging.Formatter):
    def format(self, record):
        super(JSONFormatter, self).format(record)

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
            '()': JSONFormatter
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
            "encoding": "utf-8",
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
