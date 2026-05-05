"""
PubMed collector via NCBI E-utilities (esearch + efetch).
Docs: https://www.ncbi.nlm.nih.gov/books/NBK25501/
"""
import time
import requests
from xml.etree import ElementTree as ET
from django.conf import settings

ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
EFETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"


def _params(extra):
    p = {"tool": "biomedical_corpus", "email": settings.NCBI_EMAIL}
    if settings.NCBI_API_KEY:
        p["api_key"] = settings.NCBI_API_KEY
    p.update(extra)
    return p


def search_pmids(query: str, retmax: int = 500) -> list:
    """Return up to `retmax` PubMed IDs matching the query."""
    pmids, retstart, batch = [], 0, 200
    while len(pmids) < retmax:
        size = min(batch, retmax - len(pmids))
        r = requests.get(ESEARCH, params=_params({
            "db": "pubmed", "term": query, "retmode": "json",
            "retmax": size, "retstart": retstart,
        }), timeout=30)
        r.raise_for_status()
        ids = r.json().get("esearchresult", {}).get("idlist", [])
        if not ids:
            break
        pmids.extend(ids)
        retstart += size
        time.sleep(0.34)  # NCBI rate limit (3 req/s without key)
    return pmids[:retmax]


def fetch_articles(pmids: list) -> list:
    """Return a list of dicts with parsed PubMed metadata."""
    articles = []
    for i in range(0, len(pmids), 100):
        chunk = pmids[i:i + 100]
        r = requests.get(EFETCH, params=_params({
            "db": "pubmed", "id": ",".join(chunk),
            "retmode": "xml", "rettype": "abstract",
        }), timeout=60)
        r.raise_for_status()
        root = ET.fromstring(r.content)
        for art in root.findall(".//PubmedArticle"):
            articles.append(_parse_article(art))
        time.sleep(0.34)
    return articles


def _text(node, path, default=""):
    el = node.find(path)
    return (el.text or default).strip() if el is not None and el.text else default


def _parse_article(art) -> dict:
    pmid = _text(art, ".//PMID")
    title = _text(art, ".//ArticleTitle")
    abstract = " ".join(
        (n.text or "").strip()
        for n in art.findall(".//Abstract/AbstractText") if n.text
    )
    journal = _text(art, ".//Journal/Title")
    year = _text(art, ".//PubDate/Year") or _text(art, ".//PubDate/MedlineDate")[:4]
    authors = []
    for a in art.findall(".//Author"):
        last = _text(a, "LastName")
        first = _text(a, "ForeName")
        if last or first:
            authors.append(f"{first} {last}".strip())
    mesh_terms = [
        (n.text or "").strip()
        for n in art.findall(".//MeshHeading/DescriptorName") if n.text
    ]
    keywords = [
        (n.text or "").strip()
        for n in art.findall(".//KeywordList/Keyword") if n.text
    ]
    doi = ""
    for aid in art.findall(".//ArticleId"):
        if aid.get("IdType") == "doi":
            doi = (aid.text or "").strip()
    return {
        "source": "pubmed",
        "pmid": pmid,
        "doi": doi,
        "title": title,
        "abstract": abstract,
        "journal": journal,
        "year": year,
        "authors": authors,
        "mesh_terms": mesh_terms,
        "keywords": keywords,
        "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else "",
    }
