# Biomedical Corpus — Django + MongoDB

Collecte d'un corpus de **5 000+ articles scientifiques biomédicaux** depuis :
- **PubMed** (NCBI E-utilities)
- **PubMed Central (PMC)** (full-text OA)
- **Semantic Scholar** (Graph API)

Les articles sont automatiquement classés par **domaine spécialisé** (génétique, neurosciences, immunologie, oncologie, cardiologie, microbiologie, pharmacologie, psychiatrie) via un classifieur par mots-clés / MeSH terms.

## Architecture

```
biomedical_corpus/      → Django project (settings, urls, wsgi)
articles/               → App: modèles MongoEngine + vues corpus
fetch_scripts/          → Collecteurs PubMed / PMC / Semantic Scholar + classifieur
users/                  → Auth utilisateurs
feedbacks/              → Retours utilisateurs sur articles
templates/              → HTML (Bootstrap 5)
static/                 → CSS
```

## Installation

```bash
python -m venv venv
source venv/bin/activate            # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                # éditez les valeurs
```

Démarrer **MongoDB** localement (port 27017) ou utiliser MongoDB Atlas (renseignez `MONGO_HOST`).

## Lancer

```bash
python manage.py migrate            # tables auth Django (SQLite)
python manage.py createsuperuser
python manage.py runserver
```

Ouvrir http://localhost:8000

## Construire le corpus (5 000+ articles)

```bash
# Récupérer depuis PubMed (par domaine)
python manage.py fetch_pubmed --per-domain 500

# Récupérer depuis PMC
python manage.py fetch_pmc --per-domain 200

# Récupérer depuis Semantic Scholar
python manage.py fetch_semantic_scholar --per-domain 200

# (Re)classifier le corpus
python manage.py classify_corpus

# Statistiques
python manage.py corpus_stats
```

Les commandes sont **idempotentes** (déduplication par PMID / PMCID / DOI).

## Domaines supportés

`genetique`, `neurosciences`, `immunologie`, `oncologie`, `cardiologie`,
`microbiologie`, `pharmacologie`, `psychiatrie`.

Édition possible dans `fetch_scripts/domains.py`.
