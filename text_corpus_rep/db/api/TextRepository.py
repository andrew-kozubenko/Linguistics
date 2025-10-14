from db.models import Corpus, Text

class TextRepository:
    def __init__(self):
        pass

    def collect_text(self, text: Text):
        return {
            "id": text.id,
            "title": text.title,
            "description": text.description,
            "text": text.text,
            "embedding": text.embedding,
            "corpus_id": text.corpus.id if text.corpus else None,
            "has_translation": text.has_translation.id if text.has_translation else None
        }

    def create_text(self, title, description, text, corpus_id, has_translation=None):
        corpus = Corpus.objects.get(id=corpus_id)
        t = Text.objects.create(
            title=title,
            description=description,
            text=text,
            corpus=corpus,
            has_translation=has_translation
        )
        return self.collect_text(t)

    def update_text(self, text_id, **kwargs):
        Text.objects.filter(id=text_id).update(**kwargs)
        t = Text.objects.get(id=text_id)
        t.save()
        return self.collect_text(t)

    def get_text(self, text_id):
        return self.collect_text(Text.objects.get(id=text_id))

    def delete_text(self, text_id):
        Text.objects.filter(id=text_id).delete()
        return {"deleted": True}
