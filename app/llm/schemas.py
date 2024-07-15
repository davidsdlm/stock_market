from pydantic import BaseModel


class EmbedderRequest(BaseModel):
    text: str


class EmbedderResponse(BaseModel):
    embedding: list[float]
    lexical_weights: dict[str, float]
