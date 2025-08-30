import os
from functools import lru_cache
from langdetect import detect
import numpy as np

from sentence_transformers import SentenceTransformer


@lru_cache(maxsize=1)
def get_toxicity_dummy():
    # Placeholder: return a deterministic pseudo score based on hash
    return True


def classify_toxicity(text: str) -> float:
    # Simple heuristic placeholder; replace with real transformer in models/
    h = abs(hash(text)) % 100
    return float(h) / 100.0


def classify_stance(text: str) -> str:
    # Toy stance classifier; to be replaced by transformer
    lower = text.lower()
    anti_markers = ["break india", "anti-india", "boycott india", "hate india"]
    pro_markers = ["jai hind", "pro-india", "love india", "support india"]
    if any(m in lower for m in anti_markers):
        return "anti"
    if any(m in lower for m in pro_markers):
        return "pro"
    return "neutral"


def detect_language(text: str) -> str:
    try:
        lang = detect(text)
        if lang in {"en", "hi"}:
            return lang
        return lang
    except Exception:
        return "und"


def analyze_post(text: str):
    lang = detect_language(text)
    toxicity = classify_toxicity(text)
    stance = classify_stance(text)
    return lang, toxicity, stance


@lru_cache(maxsize=1)
def get_embedding_model():
    model_name = os.getenv("EMBEDDING_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    return SentenceTransformer(model_name)


def embed_texts(texts: list[str]) -> np.ndarray:
    if not texts:
        return np.zeros((0, 384), dtype=float)
    model = get_embedding_model()
    embeddings = model.encode(texts, normalize_embeddings=True, convert_to_numpy=True)
    return embeddings


