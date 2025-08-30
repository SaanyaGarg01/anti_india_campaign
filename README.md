Anti-India Campaign Detection (Hackathon-Ready)
==============================================

Spin up with Docker and demo in minutes.

Quick Start
-----------

1. Local (no Docker) demo:

```bash
python -m venv .venv && .venv\\Scripts\\activate
pip install -r backend/requirements.txt
set DATABASE_URL=sqlite:///./aic.db
uvicorn backend.app.main:app --reload
```

Open http://localhost:8000/docs

In another terminal for the dashboard:

```bash
pip install -r frontend/requirements.txt
set API_BASE_URL=http://localhost:8000
streamlit run frontend/app.py
```

2. Docker start (optional):

```bash
docker compose up --build
```

3. Open dashboard: http://localhost:8501

4. Ingest sample data (new terminal):

```bash
curl -X POST http://localhost:8000/api/posts/ -H "Content-Type: application/json" -d @data/sample_twitter_post.json
curl -X POST http://localhost:8000/api/posts/ -H "Content-Type: application/json" -d @data/sample_reddit_post.json
curl -X POST http://localhost:8000/api/posts/ -H "Content-Type: application/json" -d @data/sample_youtube_comment.json
```

Components
----------

- Backend API: FastAPI on http://localhost:8000 (docs at /docs)
- DB: PostgreSQL (app/app) storing keywords, posts, alerts
- Graph: Neo4j (neo4j/password) capturing users, posts, hashtags
- NLP: lightweight placeholders; swap with real transformers under `backend/app/services/`
- UI: Streamlit dashboard on http://localhost:8501

Docs: see `docs/README.md` and `docs/ethics.md`.


