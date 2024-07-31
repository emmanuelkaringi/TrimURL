from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine
from fastapi.responses import RedirectResponse
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
            "short_url": f"http://localhost/{db_url.key}",
            "clicks":db_url.clicks
        }
    
    key = hashlib.md5(url.long_url.encode()).hexdigest()[:6]
    while crud.get_url_by_key(db, key):
        key = hashlib.md5((url.long_url + os.urandom(4).hex()).encode()).hexdigest()[:6]

    db_url = crud.create_url(db=db, url=url, key=key)
    return{
            "key": db_url.key,
            "long_url": db_url.long_url,
            "short_url": f"http://localhost/{db_url.key}",
            "clicks":db_url.clicks
        }

@app.get("/{url_key}", response_model=schemas.URL)
def redirect_url(url_key: str, db: Session = Depends(get_db)):
    db_url = crud.get_url_by_key(db, url_key)
    if db_url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    db_url.clicks += 1
    db.commit()
    return RedirectResponse(db_url.long_url, status_code=302)

@app.delete("/{url_key}")
def delete_url(url_key: str, db: Session = Depends(get_db)):
    db_url = crud.get_url_by_key(db, url_key)
    if db_url is None:
        raise HTTPException(status_code=404, detail ="URL not found")
    db.delete(db_url)
    db.commit()
    return{"detail": "URL deleted successfully"}