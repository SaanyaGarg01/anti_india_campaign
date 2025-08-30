from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from ..db import get_db
from .. import models

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/influencers")
def influencers(db: Session = Depends(get_db)):
    since = datetime.utcnow() - timedelta(days=3)
    q = (
        db.query(
            models.Post.author_handle,
            func.count(models.Post.id).label("posts"),
            func.avg(models.Post.toxicity).label("toxicity"),
        )
        .filter(models.Post.created_at >= since)
        .group_by(models.Post.author_handle)
        .order_by(func.count(models.Post.id).desc())
        .limit(20)
    )
    return [
        {"author": row[0], "posts": row[1], "avg_toxicity": float(row[2] or 0.0)}
        for row in q.all()
    ]


@router.get("/trends")
def trends(db: Session = Depends(get_db)):
    since = datetime.utcnow() - timedelta(hours=24)
    buckets = {}
    for p in (
        db.query(models.Post)
        .filter(models.Post.created_at >= since)
        .order_by(models.Post.created_at.asc())
        .all()
    ):
        key = p.created_at.replace(minute=(p.created_at.minute // 30) * 30, second=0, microsecond=0)
        buckets.setdefault(key.isoformat(), {"count": 0, "anti": 0, "toxicity": []})
        buckets[key.isoformat()]["count"] += 1
        buckets[key.isoformat()]["anti"] += 1 if p.stance == "anti" else 0
        buckets[key.isoformat()]["toxicity"].append(p.toxicity or 0.0)
    series = []
    for t, v in sorted(buckets.items()):
        series.append({
            "time": t,
            "count": v["count"],
            "anti_ratio": (v["anti"] / max(1, v["count"])),
            "avg_toxicity": (sum(v["toxicity"]) / max(1, len(v["toxicity"]))),
        })
    return series


