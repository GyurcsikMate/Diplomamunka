from sqlalchemy import Column, Integer, String, Float, BigInteger
from database import Base

class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    short_text = Column(String)
    url = Column(String)
    date = Column(DateTime)
    sport = Column(String)