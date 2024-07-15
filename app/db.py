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

    def execute_transaction(self, sql, data, retry_cnt):
        try:
            with self.conn.cursor() as cur:
                cur.execute(sql, data)
                self.conn.commit()
        except psycopg.errors.DeadlockDetected or psycopg.errors.SerializationFailure:
            self.conn.rollback()
            if retry_cnt > 0:
                self.execute_transaction(sql, data, retry_cnt - 1)
            else:
                raise

