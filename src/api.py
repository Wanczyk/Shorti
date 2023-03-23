from fastapi import APIRouter
from urllib.parse import urljoin
from fastapi import Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from src import crud, schemas, settings
from src.dependencies import get_db

router = APIRouter()


@router.post("/create/", response_model=schemas.ShortLink, status_code=201)
def create_short_url(link: schemas.LinkCreate, db: Session = Depends(get_db)):
    db_link = crud.create_link(db, link.original_url)
    short_link = urljoin(settings.FQDN, db_link.id)
    return schemas.ShortLink(url=short_link)


@router.get("/{link_id}", response_class=RedirectResponse)
def redirect_to_original_url(link_id: str, db: Session = Depends(get_db)):
    db_link = crud.get_original_url(db, link_id)
    if db_link is None:
        raise HTTPException(status_code=404, detail="URL not found")
    return RedirectResponse(db_link.original_url)
