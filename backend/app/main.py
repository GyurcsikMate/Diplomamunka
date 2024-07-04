from fastapi import FastAPI, HTTPException, Query, Depends
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Articles",
    description="Start using FastAPI in development",
    version="0.1"
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 


@app.get('/articles/', response_model=schemas.ArticleBase, status_code=200)
def get_article(symbol: str, db: Session = Depends(get_db)) -> models.Article:
    db_stock = crud.get_stock(db, symbol=symbol)
    if db_stock is None:
        raise HTTPException(
            status_code=404, detail=f"No stock {symbol} found."
        )

    return db_stock