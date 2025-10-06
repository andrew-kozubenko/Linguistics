from django.db import models
from db_file_storage.model_utils import delete_file, delete_file_if_needed

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
    corpus = models.ForeignKey(Corpus, on_delete=models.CASCADE, related_name="texts")
    has_translation = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='translations'
    )

    def __str__(self):
        return self.title

    