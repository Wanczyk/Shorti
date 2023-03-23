from pydantic import BaseModel


class LinkBase(BaseModel):
    original_url: str


class LinkCreate(LinkBase):
    pass


class Link(LinkBase):
    id: str

    class Config:
        orm_mode = True


class ShortLink(BaseModel):
    url: str
