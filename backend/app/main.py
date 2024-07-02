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
"""
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


"""
async def app(scope, receive, send):
    assert scope['type'] == 'http'

    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [
            [b'content-type', b'text/plain'],
        ],
    })
    await send({
        'type': 'http.response.body',
        'body': b'Hello, world!',
    })
"""

"""
beautifulsoup4
requests
psycopg2-binary
fastapi
uvicorn[standard]
sqlalchemy
"""