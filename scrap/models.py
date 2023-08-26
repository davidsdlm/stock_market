from dataclasses import dataclass


@dataclass
class News:
    url: str
    text: str
    date: str

