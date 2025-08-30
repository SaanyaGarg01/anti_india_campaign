from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import keywords, posts, alerts
from .routers import analytics
from .db import engine
from . import models

app = FastAPI(title="Cyber Threat Detection: Anti-India Campaigns", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(keywords.router, prefix="/api")
app.include_router(posts.router, prefix="/api")
app.include_router(alerts.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")

@app.get("/")
def root():
    return {"status": "ok"}


@app.on_event("startup")
def on_startup():
    # Create tables if not exist
    models.Base.metadata.create_all(bind=engine)


