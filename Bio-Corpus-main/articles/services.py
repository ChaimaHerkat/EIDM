"""
Persistence helpers: deduplicated upsert + classification.
"""
from .models import Article
from fetch_scripts.classifier import classify


def upsert_article(data: dict) -> tuple:
    """
    Insert if no existing article shares an external ID; else update missing fields.
    Returns (article, created: bool).
    """
    query = {}
    if data.get("pmid"):
        query["pmid"] = data["pmid"]
    elif data.get("pmcid"):
        query["pmcid"] = data["pmcid"]
    elif data.get("doi"):
        query["doi"] = data["doi"]
    elif data.get("ss_id"):
        query["ss_id"] = data["ss_id"]
    else:
        # No external ID — fallback to title+source uniqueness
        query["title"] = data.get("title", "")
        query["source"] = data.get("source", "")

    existing = Article.objects(**query).first() if query else None

    domain, conf = classify(
        title=data.get("title", ""),
        abstract=data.get("abstract", ""),
        mesh_terms=data.get("mesh_terms", []),
        keywords=data.get("keywords", []),
    )
    data["domain"] = domain or ""
    data["domain_confidence"] = conf

    if existing:
        for k, v in data.items():
            if v and not getattr(existing, k, None):
                setattr(existing, k, v)
        existing.save()
        return existing, False

    art = Article(**{k: v for k, v in data.items() if v is not None})
    art.save()
    return art, True
