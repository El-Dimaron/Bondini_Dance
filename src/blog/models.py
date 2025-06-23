import datetime

from mongoengine import (DateTimeField, Document, EmbeddedDocument,
                         EmbeddedDocumentField, ListField, StringField)


class Blog(EmbeddedDocument):
    name = StringField(max_length=255)
    text = StringField(max_length=2500)
    author = StringField(max_length=255)

    def __str__(self):
        return f"{self.name}"


class Entity(Document):
    blog = ListField(EmbeddedDocumentField(Blog))
    timestamp = DateTimeField(default=datetime.datetime.now())
    last_update = DateTimeField(default=datetime.datetime.now())
    headline = StringField(max_length=255)

    def __str__(self):
        return f"{self.headline}"
