from .models import News
from .db import DB


def insert_news(db: DB, data: News):
    sql = """
        INSERT INTO news (text, url, date)
        VALUES (%(url)s, %(text)s, %(date)s);
        """
    db.execute_transaction(sql, data.__dict__, 2)
