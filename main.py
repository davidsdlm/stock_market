from app.scraper import BloombergScraper
from app.llm.service import LLM
from settings import settings, Session

if __name__ == '__main__':

    llm = LLM(settings.LLM_URL)

    url = 'https://www.bloomberg.com/'
    category = 'markets/'

    bloomberg_scraper = BloombergScraper(url, category)
    news = bloomberg_scraper.scrap_news()

    response = llm.text_to_embedding(news.content)
    news.embedding = response.embedding
    news.tokens = response.lexical_weights.keys()

    with Session() as session:
        session.add(news)
        session.commit()
