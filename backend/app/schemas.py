from pydantic import BaseModel
from datetime import date, datetime, time, timedelta

class ArticleBase(BaseModel):
    title: str
    short_text: str
    url: str
    date: datetime
    sport: str

    class Config:
        orm_mode = True

