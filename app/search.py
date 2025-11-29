# app/search.py

import numpy as np
import faiss
from pathlib import Path
import pickle
from typing import List

INDEX_PATH = Path("faiss_index/index.faiss")
META_PATH = Path("faiss_index/meta.pkl")

# Dimension for sentence-transformers "all-MiniLM-L6-v2"
DIM = 384


# ========================================
# Create FAISS index
# ========================================
def create_index(embeddings: List[List[float]], metas: List[dict]):
    arr = np.array(embeddings).astype("float32")
    faiss.normalize_L2(arr)

    index = faiss.IndexFlatIP(DIM)
    index.add(arr)

    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(INDEX_PATH))

    with open(META_PATH, "wb") as f:
        pickle.dump(metas, f)


# ========================================
# Load FAISS index + meta data
# ========================================
def load_index():
    if not INDEX_PATH.exists() or not META_PATH.exists():
        return None, []

    index = faiss.read_index(str(INDEX_PATH))
    metas = pickle.load(open(META_PATH, "rb"))

    return index, metas


# ========================================
# Skill Matching Score
# ========================================
def _skill_overlap_score(query_skills, resume_skills):
    if not query_skills:
        return 0.0

    q = set(s.lower() for s in query_skills)
    r = set(s.lower() for s in resume_skills)

    if not r:
        return 0.0

    overlap = len(q & r)
    return overlap / max(len(q), 1)


# ========================================
# Experience Score
# ========================================
def _experience_score(query_years, resume_years):
    if query_years <= 0:
        return 0.0

    return min(resume_years / query_years, 1.0)


# ========================================
# Search Function
# ========================================
def search(query_embedding, k=5, query_skills=None, query_years=0):
    index, metas = load_index()
    if index is None:
        return []

    q = np.array([query_embedding]).astype("float32")
    faiss.normalize_L2(q)

    D, I = index.search(q, k)
    results = []

    for score, idx in zip(D[0], I[0]):
        if idx == -1:
            continue

        meta = metas[idx].copy()
        embed_score = float(score)

        skill_score = _skill_overlap_score(
            query_skills or [],
            meta.get("skills", [])
        )

        exp_score = _experience_score(
            query_years,
            meta.get("years_experience", 0)
        )

        # Composite Ranking Score
        composite = (
            0.55 * embed_score +
            0.25 * skill_score +
            0.15 * exp_score +
            0.05 * (len(meta.get("skills", [])) / 20)  # bonus for having more skills
        )

        meta.update({
            "embed_score": embed_score,
            "skill_score": skill_score,
            "exp_score": exp_score,
            "composite_score": composite
        })

        results.append(meta)

    # Sort by composite score (highest first)
    results = sorted(results, key=lambda x: x["composite_score"], reverse=True)

    return results
