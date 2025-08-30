from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from ..db import get_db
from .. import models, schemas
from ..services.nlp import analyze_post
from ..services.graph import GraphService

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/", response_model=schemas.PostOut)
def ingest_post(payload: schemas.PostIn, db: Session = Depends(get_db)):
    created_at = payload.created_at or datetime.utcnow()
    lang, toxicity, stance = analyze_post(payload.text)
    post = models.Post(
        id=payload.id,
        platform=payload.platform,
        author_id=payload.author_id or "",
        author_handle=payload.author_handle or "",
        text=payload.text,
        language=lang,
        toxicity=toxicity,
        stance=stance,
        hashtags=payload.hashtags,
        mentions=payload.mentions,
        meta=payload.meta,
        created_at=created_at,
    )
    db.merge(post)
    db.commit()

    GraphService().upsert_post(post)

    return post


@router.get("/", response_model=List[schemas.PostOut])
def list_posts(db: Session = Depends(get_db)):
    return db.query(models.Post).order_by(models.Post.created_at.desc()).limit(200).all()


@router.get("/{post_id}", response_model=schemas.PostOut)
def get_post(post_id: str, db: Session = Depends(get_db)):
    post = db.query(models.Post).get(post_id)
    return post


