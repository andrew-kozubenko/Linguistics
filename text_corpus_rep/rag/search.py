import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from .embeddings import embed


def search(query: str, index, top_k: int = 5):
    query_vec = embed([query])[0]

    sims = cosine_similarity(
        [query_vec],
        index["vectors"]
    )[0]

    ranked = sorted(
        zip(sims, index["meta"]),
        key=lambda x: x[0],
        reverse=True
    )

    return ranked[:top_k]
