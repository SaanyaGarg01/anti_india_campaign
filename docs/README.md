Cyber Threat Detection: Anti-India Campaigns

End-to-end system to detect and visualize anti-India influence campaigns across social platforms.

Quickstart
----------

Requirements: Docker, Docker Compose.

```bash
docker compose up --build
```

- API: http://localhost:8000
- Swagger: http://localhost:8000/docs
- Dashboard: http://localhost:8501
- Postgres: localhost:5432 (app/app)
- Neo4j: http://localhost:7474 (neo4j/password)

Demo Data
---------

Use the sample data to ingest posts:

```bash
curl -X POST http://localhost:8000/api/posts/ -H 'Content-Type: application/json' \
  -d @data/sample_twitter_post.json
```

Repeat with other files under `data/`.

Architecture
------------

- FastAPI for ingestion, processing, alerts
- PostgreSQL stores keywords and posts
- Neo4j models user/post/hashtag graph
- NLP pipeline (placeholder) classifies language, toxicity, stance
- Detection computes risk and issues alerts
- Streamlit dashboard for visualization

Development
-----------

- Edit code under `backend/` and `frontend/` volumes; containers hot-reload on restart.
- Run Alembic migrations (optional) or allow SQLAlchemy to create tables on startup.


