from django.core.management.base import BaseCommand
from fetch_scripts.domains import DOMAINS
from fetch_scripts import pubmed
from articles.services import upsert_article


class Command(BaseCommand):
    help = "Fetch articles from PubMed for each biomedical domain."

    def add_arguments(self, parser):
        parser.add_argument("--per-domain", type=int, default=500,
                            help="Articles to fetch per domain (default 500).")
        parser.add_argument("--domain", type=str, default="",
                            help="Restrict to a single domain key.")

    def handle(self, *args, **opts):
        per = opts["per_domain"]
        only = opts["domain"]
        domains = {only: DOMAINS[only]} if only else DOMAINS

        total_new, total_seen = 0, 0
        for key, cfg in domains.items():
            self.stdout.write(self.style.NOTICE(
                f"\n[PubMed] Domaine '{key}' — recherche de {per} articles..."))
            try:
                pmids = pubmed.search_pmids(cfg["query"], retmax=per)
                self.stdout.write(f"  → {len(pmids)} PMIDs trouvés. Téléchargement...")
                articles = pubmed.fetch_articles(pmids)
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"  ✗ Erreur: {e}"))
                continue

            new_count = 0
            for data in articles:
                _, created = upsert_article(data)
                total_seen += 1
                if created:
                    new_count += 1
                    total_new += 1
            self.stdout.write(self.style.SUCCESS(
                f"  ✓ {new_count} nouveaux / {len(articles)} traités"))

        self.stdout.write(self.style.SUCCESS(
            f"\n=== TERMINÉ — {total_new} nouveaux articles, {total_seen} traités ==="))
