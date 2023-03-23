from sqlalchemy import Column, String

from .database import Base


class Link(Base):
    __tablename__ = "links"

    id = Column(String, primary_key=True, index=True)
    original_url = Column(String)
