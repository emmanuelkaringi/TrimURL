from pydantic import BaseModel, HttpUrl

class URLBase(BaseModel):
    long_url: HttpUrl

class URLCreate(URLBase):
    pass

class URL(URLBase):
    key: str
    short_url: str
    clicks: int

    class Config:
        from_attributes =True