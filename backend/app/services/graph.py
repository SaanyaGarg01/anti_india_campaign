import os
from .. import models

try:
    from neo4j import GraphDatabase
    NEO4J_AVAILABLE = True
except ImportError:
    NEO4J_AVAILABLE = False
    GraphDatabase = None


class GraphService:
    def __init__(self):
        self.driver = None
        if NEO4J_AVAILABLE:
            uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
            user = os.getenv("NEO4J_USER", "neo4j")
            password = os.getenv("NEO4J_PASSWORD", "password")
            try:
                self.driver = GraphDatabase.driver(uri, auth=(user, password))
                # test connection
                with self.driver.session() as s:
                    s.run("RETURN 1")
            except Exception:
                self.driver = None

    def close(self):
        if self.driver:
            self.driver.close()

    def upsert_post(self, post: models.Post):
        if not self.driver:
            return  # Skip graph operations if Neo4j not available
        with self.driver.session() as session:
            session.execute_write(self._upsert_post_tx, post)

    @staticmethod
    def _upsert_post_tx(tx, post: models.Post):
        tx.run(
            """
            MERGE (u:User {id: $author_id})
            SET u.handle = $author_handle
            MERGE (p:Post {id: $post_id})
            SET p.platform = $platform, p.text = $text, p.language=$language, p.toxicity=$toxicity, p.stance=$stance, p.created_at=$created_at
            MERGE (u)-[:POSTED]->(p)
            FOREACH (h IN $hashtags | MERGE (t:Hashtag {name: toLower(h)}) MERGE (p)-[:TAGGED]->(t))
            """,
            author_id=post.author_id,
            author_handle=post.author_handle,
            post_id=post.id,
            platform=post.platform,
            text=post.text[:1000],
            language=post.language,
            toxicity=post.toxicity,
            stance=post.stance,
            created_at=post.created_at.isoformat(),
            hashtags=post.hashtags or [],
        )


