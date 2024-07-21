import requests
import urllib.parse

from app.search import schemas


class Search:
    def __init__(self, url: str):
        self.url = url

    def search_by_vector(self, embedding: list[float], n: int = 10):
        data = schemas.SearchVectorRequest(embedding=embedding, n=n)
        url = urllib.parse.urljoin(self.url, "search_by_vector/")
        res = requests.post(url, json=data.model_dump()).json()
        return schemas.SearchResponse(**res)

    def search_by_token(self, tokens: list[str], n: int = 10):
        data = schemas.SearchTokensRequest(embedding=tokens, n=n)
        url = urllib.parse.urljoin(self.url, "search_by_token/")
        res = requests.post(url, json=data.model_dump()).json()
        return schemas.SearchResponse(**res)
