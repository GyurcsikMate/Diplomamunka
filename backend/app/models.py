#from sqlalchemy import Column, Integer, String, DateTime
from database import Base, Field


class Article(Base):
    __tablename__ = 'articles'
    id = Field(...)
    title = Field(...)
    short_text = Field(...)
    url = Field(...)
    date = Field(...)
    sport = Field(...)