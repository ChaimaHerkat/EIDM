"""
MongoEngine document for biomedical articles.
Stored in MongoDB collection `articles`.
"""
from datetime import datetime
import mongoengine as me


class Article(me.Document):
    # External identifiers (any can be empty)
    pmid = me.StringField(default="")
    pmcid = me.StringField(default="")
    doi = me.StringField(default="")
    ss_id = me.StringField(default="")  # Semantic Scholar ID

    # Content
    title = me.StringField(required=True)
    abstract = me.StringField(default="")
    journal = me.StringField(default="")
    year = me.StringField(default="")
    authors = me.ListField(me.StringField(), default=list)
    mesh_terms = me.ListField(me.StringField(), default=list)
    keywords = me.ListField(me.StringField(), default=list)

    # Source + classification
    source = me.StringField(choices=["pubmed", "pmc", "semantic_scholar"], required=True)
    domain = me.StringField(default="")           # e.g. "neurosciences"
    domain_confidence = me.FloatField(default=0.0)

    url = me.StringField(default="")
    fetched_at = me.DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "articles",
        "indexes": [
            "pmid", "pmcid", "doi", "ss_id", "domain", "source", "year",
            {"fields": ["$title", "$abstract"], "default_language": "english"},
        ],
        "ordering": ["-fetched_at"],
    }

    def __str__(self):
        return f"[{self.source}] {self.title[:80]}"

    @property
    def best_id(self):
        return self.pmid or self.pmcid or self.doi or self.ss_id or str(self.id)
