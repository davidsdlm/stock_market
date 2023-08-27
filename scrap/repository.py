from .models import News
from .db import DB


def retry_policy(retry_cnt=0):
    def retry_decorator(func):
        def _wrapper(db: DB, *args, **kwargs):
            def _new_func(retry_cnt):
                with db(_new_func, retry_cnt, *args, **kwargs) as cnt:
                    return func(db, *args, **kwargs)

            return _new_func(retry_cnt)

        return _wrapper

    return retry_decorator


@retry_policy()
def insert_news(db: DB, data: News):
    sql = """
        INSERT INTO news (url, text, date)
        VALUES (%(url)s, %(text)s, %(date)s);
        """

    db.conn.cursor().execute(sql, data.__dict__)
