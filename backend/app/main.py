from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine
import hashlib
import os

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/", response_model=schemas.URL)
def create_short_url(url: schemas.URLCreate, db:Session = Depends(get_db)):
    db_url = crud.get_url_by_long_url(db, long_url=url.long_url)
    if db_url:
        return{
            "key": db_url.key,
            "long_url": db_url.long_url,
            "short_url": f"http://localhost/{db_url.key}"
        }
    
    key = hashlib.md5(url.long_url.encode()).hexdigest()[:6]
    while crud.get_url_by_key(db, key):
        key = hashlib.md5((url.long_url + os.urandom(4).hex()).encode()).hexdigest()[:6]

    db_url = crud.create_url(db=db, url=url, key=key)
    return{
            "key": db_url.key,
            "long_url": db_url.long_url,
            "short_url": f"http://localhost/{db_url.key}"
        }