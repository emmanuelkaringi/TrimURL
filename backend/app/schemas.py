from pydantic import BaseModel

class URLBase(BaseModel):
    long_url: str

class URLCreate(URLBase):
    pass

class URL(URLBase):
    key: str
    short_url: str

    class Config:
        from_attributes =True