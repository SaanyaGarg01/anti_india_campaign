from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import math
from collections import defaultdict

from .. import models
from .nlp import embed_texts


def compute_risk(posts: list[models.Post]) -> float:
    if not posts:
        return 0.0
    toxicity = sum(p.toxicity or 0.0 for p in posts) / len(posts)
    anti_ratio = sum(1.0 if (p.stance == "anti") else 0.0 for p in posts) / len(posts)
    volume = min(len(posts) / 50.0, 1.0)
    return float((0.5 * toxicity + 0.4 * anti_ratio + 0.1 * volume) * 100.0)


def evaluate_alerts(db: Session):
    since = datetime.utcnow() - timedelta(hours=6)
    recent = (
        db.query(models.Post)
        .filter(models.Post.created_at >= since)
        .all()
    )

    # Group by top hashtag
    groups: dict[str, list[models.Post]] = {}
    for p in recent:
        top = (p.hashtags or ["uncategorized"])[0] if p.hashtags else "uncategorized"
        groups.setdefault(top, []).append(p)

    for tag, posts in groups.items():
        risk = compute_risk(posts)
        burst = burst_score(posts)
        coord = coordination_score(posts)
        bot = bot_likelihood(posts)
        total = min(100.0, 0.5 * risk + 0.2 * burst + 0.2 * coord + 0.1 * bot)
        if total >= 60:
            alert = models.Alert(
                name=f"Spike around #{tag}",
                risk_score=total,
                details={
                    "hashtag": tag,
                    "count": len(posts),
                    "scores": {"risk": risk, "burst": burst, "coordination": coord, "bot": bot},
                },
            )
            db.add(alert)
    db.commit()


def get_campaign_details(db: Session, campaign_id: int):
    alert = db.query(models.Alert).get(campaign_id)
    if not alert:
        return {"error": "not_found"}
    tag = alert.details.get("hashtag", "") if alert.details else ""
    posts = []
    if tag:
        posts = (
            db.query(models.Post)
            .filter(models.Post.hashtags.contains([tag]))
            .order_by(models.Post.created_at.desc())
            .limit(200)
            .all()
        )
    return {
        "alert": {
            "id": alert.id,
            "name": alert.name,
            "risk_score": alert.risk_score,
            "created_at": alert.created_at,
        },
        "sample_posts": [
            {
                "id": p.id,
                "text": p.text,
                "stance": p.stance,
                "toxicity": p.toxicity,
                "created_at": p.created_at,
            }
            for p in posts
        ],
    }


def burst_score(posts: list[models.Post]) -> float:
    if not posts:
        return 0.0
    timestamps = sorted([p.created_at.timestamp() for p in posts])
    if len(timestamps) <= 1:
        return 0.0
    intervals = [timestamps[i+1] - timestamps[i] for i in range(len(timestamps)-1)]
    mu = sum(intervals) / len(intervals)
    variance = sum((x - mu)**2 for x in intervals) / len(intervals)
    sigma = math.sqrt(variance) + 1e-6
    z = max(0.0, (3600.0 - mu) / sigma)  # smaller mean interval => higher burst
    return float(min(100.0, 20.0 * z))


def coordination_score(posts: list[models.Post]) -> float:
    if len(posts) < 3:
        return 0.0
    texts = [p.text for p in posts]
    emb = embed_texts(texts)
    if len(emb) < 3:
        return 0.0
    
    n = len(emb)
    # fraction of pairs with similarity > 0.85 within 15 minutes
    times = [p.created_at.timestamp() for p in posts]
    coord_pairs = 0
    total_pairs = max(1, n * (n - 1) // 2)
    
    for i in range(n):
        for j in range(i + 1, n):
            # cosine similarity
            dot = sum(emb[i][k] * emb[j][k] for k in range(len(emb[i])))
            sim = max(0.0, min(1.0, dot))
            if sim > 0.85 and abs(times[i] - times[j]) <= 900:
                coord_pairs += 1
    
    frac = coord_pairs / total_pairs
    return float(min(100.0, 100.0 * frac))


def bot_likelihood(posts: list[models.Post]) -> float:
    if not posts:
        return 0.0
    by_user = defaultdict(list)
    for p in posts:
        by_user[p.author_id].append(p)
    # user-level bot score: high frequency and repetitive content (cosine sim mean)
    user_scores = []
    for user, uposts in by_user.items():
        if len(uposts) < 2:
            continue
        times = sorted([p.created_at.timestamp() for p in uposts])
        freq = len(uposts) / max(1.0, (times[-1] - times[0]) / 3600.0)
        texts = [p.text for p in uposts]
        emb = embed_texts(texts)
        if len(emb) >= 2:
            # calculate pairwise similarity
            sims = []
            for i in range(len(emb)):
                for j in range(i + 1, len(emb)):
                    dot = sum(emb[i][k] * emb[j][k] for k in range(len(emb[i])))
                    sims.append(max(0.0, min(1.0, dot)))
            rep = sum(sims) / len(sims) if sims else 0.0
        else:
            rep = 0.0
        score = min(100.0, 20.0 * freq + 80.0 * rep)
        user_scores.append(score)
    if not user_scores:
        return 0.0
    return float(sum(user_scores) / len(user_scores))


