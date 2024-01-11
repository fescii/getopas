# documents.py
from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import Issue

@registry.register_document
class IssueDocument(Document):
    class Index:
        name = 'issue'
        settings = {
        'number_of_shards': 1,
        'number_of_replicas': 0
    }
    class Django:
         model = Issue
         fields = [
             'title',
             'description',
             'owner',
         ]