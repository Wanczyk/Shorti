from sqlalchemy.orm import Session

from . import models
from .utils import generate_id


def get_original_url(db: Session, link_id: str):
    return db.query(models.Link).filter(models.Link.id == link_id).first()


def create_link(db: Session, original_url: str):
    link_id = generate_id()
    while db.query(models.Link).filter(models.Link.id == link_id).first():
        link_id = generate_id()

    db_link = models.Link(id=link_id, original_url=original_url)
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    return db_link
