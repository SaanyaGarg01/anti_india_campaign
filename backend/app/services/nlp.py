import os
from functools import lru_cache
import hashlib
import math


@lru_cache(maxsize=1)
def get_toxicity_dummy():
    # Placeholder: return a deterministic pseudo score based on hash
    return True


def classify_toxicity(text: str) -> float:
    # Simple heuristic placeholder; replace with real transformer in models/
    h = abs(hash(text)) % 100
    return float(h) / 100.0


def classify_stance(text: str) -> str:
    # Enhanced stance classifier with more keywords
    lower = text.lower()
    
    # Anti-India markers
    anti_markers = [
        "break india", "anti-india", "boycott india", "hate india", "destroy india",
        "india bad", "corrupt india", "fake india", "fascist india", "terrorist india",
        "against india", "down with india", "stop india", "end india", "ban india",
        "india enemy", "india threat", "india problem", "india danger", "india evil"
    ]
    
    # Pro-India markers  
    pro_markers = [
        "jai hind", "pro-india", "love india", "support india", "incredible india",
        "proud india", "great india", "strong india", "rising india", "shining india",
        "india great", "vande mataram", "bharat mata", "india rocks", "go india",
        "india forever", "india zindabad", "unity in diversity", "digital india"
    ]
    
    # Neutral/discussion markers
    neutral_markers = [
        "discuss india", "debate about india", "india analysis", "india review",
        "india opinion", "india perspective", "india situation", "india policy"
    ]
    
    anti_score = sum(1 for marker in anti_markers if marker in lower)
    pro_score = sum(1 for marker in pro_markers if marker in lower)
    neutral_score = sum(1 for marker in neutral_markers if marker in lower)
    
    if anti_score > pro_score and anti_score > neutral_score:
        return "anti"
    elif pro_score > anti_score and pro_score > neutral_score:
        return "pro"
    else:
        return "neutral"


def detect_language(text: str) -> str:
    # Simple heuristic language detection
    hindi_chars = sum(1 for c in text if '\u0900' <= c <= '\u097F')
    total_chars = len([c for c in text if c.isalpha()])
    if total_chars > 0 and hindi_chars / total_chars > 0.3:
        return "hi"
    return "en"


def analyze_post(text: str):
    lang = detect_language(text)
    toxicity = classify_toxicity(text)
    stance = classify_stance(text)
    return lang, toxicity, stance


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Placeholder embedding using simple text hashing"""
    if not texts:
        return []
    
    embeddings = []
    for text in texts:
        # Simple hash-based embedding for demo
        h = abs(hash(text.lower()))
        vec = [float((h >> i) & 1) * 2 - 1 for i in range(64)]
        norm = math.sqrt(sum(x*x for x in vec))
        if norm > 0:
            vec = [x/norm for x in vec]
        embeddings.append(vec)
    
    return embeddings


