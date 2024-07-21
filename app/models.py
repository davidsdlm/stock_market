from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.types import ARRAY, String, Float


class Base(DeclarativeBase):
    pk: Mapped[str] = mapped_column(primary_key=True)
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date: Mapped[datetime] = mapped_column(server_default=func.now())
    content: Mapped[str]
    tokens = mapped_column(ARRAY(String))
    embedding = mapped_column(ARRAY(Float))


class Companies(Base):
    __tablename__ = "companies"


class News(Base):
    __tablename__ = "news"
