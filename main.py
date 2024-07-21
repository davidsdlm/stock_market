from datetime import timedelta, datetime

from airflow.decorators import dag, task

from app.llm.service import LLM
from app.scraper import BloombergScraper
from app.search.service import Search
from settings import settings

docker_kwargs = {
    "retries": 1,
    "docker_url": "tcp://host.docker.internal:2375",
    "network_mode": "bridge",
    "auto_remove": True,
}


@dag(
    dag_id="finances",
    schedule_interval=timedelta(days=1),
    start_date=datetime.now(),
    dagrun_timeout=timedelta(minutes=5),
)
def finances():
    @task.docker(image="my_airflow_image", **docker_kwargs, env_file=".env", mem_limit=2, cpus=1, )
    def scrap_news():

        llm = LLM(settings.LLM_URL)
        search = Search(settings.SEARCH_URL)

        url = 'https://www.bloomberg.com/'
        category = 'markets/'

        bloomberg_scraper = BloombergScraper(url, category)
        news = bloomberg_scraper.scrap_news()

        response = llm.text_to_embedding(news.content)
        news.embedding = response.embedding
        news.tokens = list(response.lexical_weights.keys())

        vector_search_ids = search.search_by_vector(news.embedding)
        token_search_ids = search.search_by_token(news.tokens)

    scrap_news()


finances()
