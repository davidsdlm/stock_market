import requests
import urllib.parse

from app.llm import schemas


class LLM:
    def __init__(self, url: str):
        self.url = url

    def text_to_embedding(self, text: str) -> schemas.EmbedderResponse:
        data = schemas.EmbedderRequest(text=text)
        url = urllib.parse.urljoin(self.url, "embed/")
        res = requests.post(url, json=data.model_dump()).json()
        return schemas.EmbedderResponse(**res)
