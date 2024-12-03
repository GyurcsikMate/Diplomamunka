from sqlalchemy.orm import Session

import models, schemas

def get_article(db: Session, symbol: str):
    return db.query(models.Article).first()