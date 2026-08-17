from dataclasses import dataclass
from datetime import datetime


@dataclass
class Post:
    id: str
    title: str
    text: str
    network: str
    publish_date: datetime | None
    status: str
    media: list[str]
