# app/embedder.py
import os
from typing import List

MODE = os.getenv("EMBED_MODE", "local")  # set EMBED_MODE=openai to use OpenAI

if MODE == "openai":
    import openai
    openai.api_key = os.getenv("OPENAI_API_KEY")

    def embed_texts(texts: List[str]) -> List[List[float]]:
        res = openai.Embedding.create(model="text-embedding-3-small", input=texts)
        return [r["embedding"] for r in res["data"]]

else:
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer('all-MiniLM-L6-v2')  # 384-dim model

    def embed_texts(texts: List[str]) -> List[List[float]]:
        return model.encode(texts, show_progress_bar=False).tolist()
