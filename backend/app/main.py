#python -m pip install -r requirements.txt
from fastapi import FastAPI
#from sqlalchemy import create_engine
#from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.orm import sessionmaker
import os
"""
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
"""
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}