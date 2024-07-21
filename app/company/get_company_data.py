import pandas as pd
import yfinance as yf

from app.llm.service import LLM
from settings import settings, Session

data = pd.read_csv("data/info.csv")


def get_company_info(ticker: str) -> str | None:
    try:
        data = yf.Ticker(ticker)
        return data.info["longBusinessSummary"]
    except Exception as e:
        print(e)
        return None


llm = LLM(settings.LLM_URL)
# news.embedding = response.embedding
# news.tokens = response.lexical_weights.keys()
#
# with Session() as session:
#     session.add(news)
#     session.commit()


# data["info"] = data["Ticker"].apply(get_company_info)
data = data.dropna()
processed_company = [llm.text_to_embedding(content) for content in data["info"].values]
embeddings = [company.embedding for company in processed_company]
tokens = [company.lexical_weights.keys() for company in processed_company]
data["embedding"] = embeddings
data["tokens"] = tokens
data.to_csv("data/processed_company.csv")
