import numpy as np
from django.db import models
from db_file_storage.model_utils import delete_file, delete_file_if_needed
from sentence_transformers import SentenceTransformer

from db.api.embedding_utils import get_chunks, get_embeddings

model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-mpnet-base-v2')

class Test(models.Model):
    name = models.TextField()

    def __str__(self):
        return self.name  # Returns the value of the 'name' field

class Corpus(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    genre = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Text(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    text = models.TextField()
    embedding = models.JSONField(null=True, blank=True)
    corpus = models.ForeignKey(Corpus, on_delete=models.CASCADE, related_name="texts")
    has_translation = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='translations'
    )

    def save(self, *args, **kwargs):
        """
        При сохранении объекта автоматически вычисляем эмбеддинг текста.
        Используются функции get_chunks() и get_embeddings().
        """
        if self.text:
            # Разбиваем текст на фрагменты
            chunks = get_chunks(self.text)

            # Получаем эмбеддинги для фрагментов
            embeddings = get_embeddings(chunks)

            # Усредняем эмбеддинги, чтобы получить один вектор
            mean_emb = np.mean(embeddings, axis=0)

            # Преобразуем в список (для JSONField)
            self.embedding = mean_emb.tolist()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    