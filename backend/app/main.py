#import  models, schemas
from fastapi import FastAPI, Body
from pymongo import MongoClient, ReturnDocument
import os
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from bson import ObjectId
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator
from bson import json_util, ObjectId
import json
import motor.motor_asyncio

def parse_json(data):
    return json.loads(json_util.dumps(data))


PyObjectId = Annotated[str, BeforeValidator(str)]

class Article(BaseModel):
    __tablename__ = 'articles'
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title:str = Field(...)
    short_text:str = Field(...)
    url:str = Field(...)
    date:str = Field(...)
    sport:str = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )


app = FastAPI()

MONGO_DETAILS = os.getenv("MONGO_DETAILS", "mongodb://mongodb:27017")
client = MongoClient(MONGO_DETAILS)
database = client['test_database']
collection = database['articles']

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/articles/{article_id}")
def read_article(article_id: int):
    article = collection.find_one({"article_id": article_id})
    if article:
        return {"article_id": article_id, "value": article["value"]}
    return {"error": "Item not found"}

@app.get("/articles", response_model=list[Article])
def read_articles():
    articles =  collection.find()
    if articles:
        return articles
    return {"error": "Item not found"}

@app.post("/articles")
def insert_user(article:Article= Body(...)):
    result =  collection.insert_one(article.model_dump(by_alias=True, exclude=["id"]))
    inserted_article =  collection.find_one({"_id": result.inserted_id})
    return inserted_article







"""
@app.get('/articles/', response_model=schemas.ArticleBase, status_code=200)
def get_article(symbol: str, db: Session = Depends(get_db)) -> models.Article:
    db_stock = crud.get_stock(db, symbol=symbol)
    if db_stock is None:
        raise HTTPException(
            status_code=404, detail=f"No stock {symbol} found."
        )

    return db_stock
"""