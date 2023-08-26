import psycopg
from dataclasses import dataclass


@dataclass
class DBInfo:
    dbname: str
    user: str
    password: str
    host: str
    port: int


class DB:
    def __init__(self, db_info: DBInfo):
        self.db_info = db_info
        self.conn: psycopg.Connection = None

    def start_up(self):
        self.conn = psycopg.connect(**self.db_info.__dict__)

    def shut_down(self):
        self.conn.close()

    def __call__(self, func, retry_cnt, *args, **kwargs):
        self.func = func
        self.retry_cnt = retry_cnt
        self.args = args
        self.kwargs = kwargs
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            self.conn.rollback()
        else:
            self.conn.commit()
        if exc_type == psycopg.errors.DeadlockDetected or exc_type == psycopg.errors.SerializationFailure:
            if self.retry_cnt > 0:
                self.func(self.retry_cnt - 1)
