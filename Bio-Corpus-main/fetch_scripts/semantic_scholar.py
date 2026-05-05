"""
Semantic Scholar Graph API collector.
Docs: https://api.semanticscholar.org/api-docs/graph
"""
import time
import requests
from django.conf import settings

SEARCH_URL = "https://api.semanticscholar.org/graph/v1/paper/search"

FIELDS = "paperId,externalIds,title,abstract,year,authors,venue,fieldsOfStudy"


def _headers():
    h = {"User-Agent": "biomedical_corpus/1.0"}
    if settings.SEMANTIC_SCHOLAR_API_KEY:
        h["x-api-key"] = settings.SEMANTIC_SCHOLAR_API_KEY
    return h


def search(query: str, limit: int = 200) -> list:
    """Paginate Semantic Scholar relevance search (max 100 per page)."""
    results, offset, page = [], 0, 100
    while len(results) < limit:
        size = min(page, limit - len(results))
        r = requests.get(SEARCH_URL, headers=_headers(), params={
            "query": query, "limit": size, "offset": offset, "fields": FIELDS,
        }, timeout=30)
        if r.status_code == 429:
            time.sleep(5)
            continue
        r.raise_for_status()
        data = r.json().get("data", [])
        if not data:
            break
        results.extend(data)
        offset += size
        if offset >= 1000:  # API hard limit on offset
            break
        time.sleep(1.1)  # public rate limit
    return _normalize(results[:limit])


def _normalize(items: list) -> list:
    out = []
    for it in items:
        ext = it.get("externalIds") or {}
        out.append({
            "source": "semantic_scholar",
            "ss_id": it.get("paperId", ""),
            "doi": ext.get("DOI", "") or "",
            "pmid": ext.get("PubMed", "") or "",
            "pmcid": ext.get("PubMedCentral", "") or "",
            "title": it.get("title") or "",
            "abstract": it.get("abstract") or "",
            "journal": it.get("venue") or "",
            "year": str(it.get("year") or ""),
            "authors": [a.get("name", "") for a in (it.get("authors") or [])],
            "mesh_terms": [],
            "keywords": it.get("fieldsOfStudy") or [],
            "url": f"https://www.semanticscholar.org/paper/{it.get('paperId','')}",
        })
    return out
