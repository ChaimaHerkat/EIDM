"""
Keyword + MeSH-based classifier. Returns the best-matching domain key
and a confidence score in [0, 1]. Falls back to None if no signal.
"""
from collections import defaultdict
from .domains import DOMAINS


def classify(title: str = "", abstract: str = "", mesh_terms=None, keywords=None):
    text = " ".join([
        (title or ""),
        (abstract or ""),
        " ".join(mesh_terms or []),
        " ".join(keywords or []),
    ]).lower()

    if not text.strip():
        return None, 0.0

    scores = defaultdict(int)
    for domain_key, cfg in DOMAINS.items():
        for kw in cfg["keywords"]:
            kw_l = kw.lower()
            if kw_l in text:
                # weight: title hits worth more
                weight = 3 if kw_l in (title or "").lower() else 1
                scores[domain_key] += weight

    if not scores:
        return None, 0.0

    best = max(scores.items(), key=lambda x: x[1])
    total = sum(scores.values())
    confidence = best[1] / total if total else 0.0
    return best[0], round(confidence, 3)
