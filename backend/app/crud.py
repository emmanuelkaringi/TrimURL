from sqlalchemy.orm import Session
from . import models, schemas

def get_url_by_key(db: Session, key: str):
    return db.query(models.URL).filter(models.URL.key == key).first()

def get_url_by_long_url(db: Session, long_url: str):
    return db.query(models.URL).filter(models.URL.long_url == long_url).first()

def create_url(db: Session, url: schemas.URLCreate, key: str):
    db_url = models.URL(key=key, long_url=url.long_url)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url