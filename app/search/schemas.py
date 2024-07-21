from pydantic import BaseModel
from pydantic import Field


class SearchVectorRequest(BaseModel):
    embedding: list[float] = Field(min_length=1024, max_length=1024)
    n: int = 10


class SearchResponse(BaseModel):
    company_ids: list[int]


class SearchTokensRequest(BaseModel):
    tokens: list[str] = Field(min_length=1024, max_length=1024)
    n: int = 10



