from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer

BASE = Path(__file__).parent.parent
KB = BASE / "data" / "knowledge_base.txt"
_model = None


def _get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")
    return _model


def _load_chunks():
    blocks = [b.strip() for b in KB.read_text(encoding="utf-8").split("\n\n") if b.strip()]
    chunks = []
    for block in blocks:
        lines = block.splitlines()
        title = lines[0].replace("TITLE:", "").strip()
        content = "\n".join(lines[1:]).replace("CONTENT:", "").strip()
        chunks.append({"title": title, "content": content})
    return chunks


def retrieve_knowledge(query: str, top_k: int = 2):
    chunks = _load_chunks()
    model = _get_model()
    texts = [c["content"] for c in chunks]
    embeddings = model.encode([query] + texts, normalize_embeddings=True)
    scores = np.dot(embeddings[1:], embeddings[0])
    ranked = np.argsort(scores)[::-1][:top_k]
    return [
        {"title": chunks[i]["title"], "content": chunks[i]["content"], "score": float(scores[i])}
        for i in ranked
    ]
