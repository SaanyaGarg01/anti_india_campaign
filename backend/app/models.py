from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, ForeignKey, Float, Index
from sqlalchemy.orm import relationship
from datetime import datetime

from .db import Base


class Keyword(Base):
    __tablename__ = "keywords"
    id = Column(Integer, primary_key=True, index=True)
    term = Column(String(256), unique=True, index=True, nullable=False)
    category = Column(String(64), default="general", index=True)
    description = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)


class Post(Base):
    __tablename__ = "posts"
    id = Column(String(128), primary_key=True)
    platform = Column(String(32), index=True)  # twitter, reddit, youtube
    author_id = Column(String(128), index=True)
    author_handle = Column(String(256))
    text = Column(Text)
    language = Column(String(16))
    toxicity = Column(Float)
    stance = Column(String(16))  # pro, anti, neutral
    hashtags = Column(JSON, default=list)
    mentions = Column(JSON, default=list)
    meta = Column(JSON, default=dict)  # likes, retweets, etc
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    __table_args__ = (
        Index("ix_posts_platform_created", "platform", "created_at"),
    )


class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(256), nullable=False)
    risk_score = Column(Float, default=0.0)
    details = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)


