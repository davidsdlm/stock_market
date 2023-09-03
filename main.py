from scrap import BloombergScraper
from scrap import DBInfo
from scrap import Service

if __name__ == '__main__':
    db_info = DBInfo(
        dbname='db',
        user='user',
        password='pg',
        host='localhost',
        port=5432
    )

    interval = 60
    url = 'https://www.bloomberg.com'
    category = 'markets'

    bloomberg_scraper = BloombergScraper(url, category)
    with Service(bloomberg_scraper, db_info, interval) as bloomberg:
        bloomberg()
        input()
