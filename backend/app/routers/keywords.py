from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from ..db import get_db
from .. import models, schemas

router = APIRouter(prefix="/keywords", tags=["keywords"])


@router.post("/", response_model=schemas.KeywordOut)
def create_keyword(payload: schemas.KeywordCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Keyword).filter(models.Keyword.term == payload.term).first()
    if existing:
        raise HTTPException(status_code=409, detail="Term already exists")
    kw = models.Keyword(term=payload.term, category=payload.category, description=payload.description)
    db.add(kw)
    db.commit()
    db.refresh(kw)
    return kw


@router.get("/", response_model=List[schemas.KeywordOut])
def list_keywords(q: str | None = Query(default=None), db: Session = Depends(get_db)):
    query = db.query(models.Keyword)
    if q:
        pattern = f"%{q}%"
        query = query.filter(models.Keyword.term.ilike(pattern))
    return query.order_by(models.Keyword.created_at.desc()).all()


@router.delete("/{keyword_id}")
def delete_keyword(keyword_id: int, db: Session = Depends(get_db)):
    kw = db.query(models.Keyword).get(keyword_id)
    if not kw:
        raise HTTPException(status_code=404, detail="Not found")
    db.delete(kw)
    db.commit()
    return {"deleted": True}


