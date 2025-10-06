from db.models import Corpus

class CorpusRepository:
    def __init__(self):
        pass

    def collect_corpus(self, corpus: Corpus):
        return {
            "id": corpus.id,
            "title": corpus.title,
            "description": corpus.description,
            "genre": corpus.genre,
            "texts": [
                {
                    "id": t.id,
                    "title": t.title,
                    "description": t.description,
                    "text": t.text,
                    "has_translation": t.has_translation.id if t.has_translation else None
                }
                for t in corpus.texts.all()
            ]
        }

    def create_corpus(self, title, description, genre):
        corpus = Corpus.objects.create(title=title, description=description, genre=genre)
        return self.collect_corpus(corpus)

    def update_corpus(self, corpus_id, **kwargs):
        Corpus.objects.filter(id=corpus_id).update(**kwargs)
        corpus = Corpus.objects.get(id=corpus_id)
        return self.collect_corpus(corpus)

    def get_corpus(self, corpus_id):
        corpus = Corpus.objects.prefetch_related("texts").get(id=corpus_id)
        return self.collect_corpus(corpus)

    def delete_corpus(self, corpus_id):
        Corpus.objects.filter(id=corpus_id).delete()
        return {"deleted": True}
