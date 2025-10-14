from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re

# Загружаем модель один раз
model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')

def get_chunks(text: str, chunk_size: int = 200) -> list[str]:
    """
    Разбивает текст на чанки длиной примерно chunk_size слов.
    """
    words = re.findall(r'\w+', text)
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = ' '.join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

def get_embeddings(texts: list[str]) -> np.ndarray:
    """
    Возвращает эмбеддинги для списка текстов (или чанков).
    """
    return model.encode(texts, convert_to_numpy=True)

def cos_compare(emb1: np.ndarray, emb2: np.ndarray) -> float:
    """
    Вычисляет косинусное сходство между двумя эмбеддингами.
    """
    emb1 = emb1.reshape(1, -1)
    emb2 = emb2.reshape(1, -1)
    return float(cosine_similarity(emb1, emb2)[0][0])
