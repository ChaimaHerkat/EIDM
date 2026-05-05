"""
PubMed Central (PMC) collector — Open Access subset via E-utilities.
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


def search_pmcids(query: str, retmax: int = 200) -> list:
    """Search the PMC OA subset."""
    full_query = f'({query}) AND "open access"[filter]'
    pmcids, retstart, batch = [], 0, 200
    while len(pmcids) < retmax:
        size = min(batch, retmax - len(pmcids))
        r = requests.get(ESEARCH, params=_params({
            "db": "pmc", "term": full_query, "retmode": "json",
            "retmax": size, "retstart": retstart,
        }), timeout=30)
        r.raise_for_status()
        ids = r.json().get("esearchresult", {}).get("idlist", [])
        if not ids:
            break
        pmcids.extend(ids)
        retstart += size
        time.sleep(0.34)
    return pmcids[:retmax]


def fetch_articles(pmcids: list) -> list:
    articles = []
    for i in range(0, len(pmcids), 50):
        chunk = pmcids[i:i + 50]
        r = requests.get(EFETCH, params=_params({
            "db": "pmc", "id": ",".join(chunk), "retmode": "xml",
        }), timeout=90)
        r.raise_for_status()
        try:
            root = ET.fromstring(r.content)
        except ET.ParseError:
            continue
        for art in root.findall(".//article"):
            articles.append(_parse(art))
        time.sleep(0.34)
    return articles


def _all_text(node):
    return " ".join(node.itertext()).strip() if node is not None else ""


def _parse(art) -> dict:
    pmcid = ""
    for aid in art.findall(".//article-id"):
        if aid.get("pub-id-type") == "pmc":
            pmcid = (aid.text or "").strip()
    pmid = ""
    doi = ""
    for aid in art.findall(".//article-id"):
        t = aid.get("pub-id-type")
        if t == "pmid":
            pmid = (aid.text or "").strip()
        elif t == "doi":
            doi = (aid.text or "").strip()

    title = _all_text(art.find(".//title-group/article-title"))
    abstract = _all_text(art.find(".//abstract"))
    journal = _all_text(art.find(".//journal-title"))
    year = ""
    pdate = art.find(".//pub-date/year")
    if pdate is not None and pdate.text:
        year = pdate.text.strip()

    authors = []
    for c in art.findall(".//contrib[@contrib-type='author']"):
        sn = c.find(".//surname")
        gn = c.find(".//given-names")
        name = f"{(gn.text or '') if gn is not None else ''} {(sn.text or '') if sn is not None else ''}".strip()
        if name:
            authors.append(name)

    keywords = [
        (k.text or "").strip()
        for k in art.findall(".//kwd-group/kwd") if k.text
    ]

    return {
        "source": "pmc",
        "pmid": pmid,
        "pmcid": f"PMC{pmcid}" if pmcid and not pmcid.startswith("PMC") else pmcid,
        "doi": doi,
        "title": title,
        "abstract": abstract,
        "journal": journal,
        "year": year,
        "authors": authors,
        "mesh_terms": [],
        "keywords": keywords,
        "url": f"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{pmcid}/" if pmcid else "",
    }
