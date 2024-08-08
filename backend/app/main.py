#import  models, schemas
from fastapi import FastAPI
from pymongo import MongoClient
import os

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

@app.get("/articles")
def read_articles():
    articles = collection.find()
    if articles:
        return articles
    return {"error": "Item not found"}

@app.get("/articles/{article_id}")
def insert_user(user: User):
    result = await app.mongodb["users"].insert_one(user.dict())
    inserted_user = await app.mongodb["users"].find_one({"_id": result.inserted_id})
    return inserted_user
def read_article(article_id: int):
    article = collection.find_one({"article_id": article_id})
    if article:
        return {"article_id": article_id, "value": article["value"]}
    return {"error": "Item not found"}






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