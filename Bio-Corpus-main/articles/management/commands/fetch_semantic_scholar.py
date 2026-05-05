from django.core.management.base import BaseCommand
from fetch_scripts.domains import DOMAINS
from fetch_scripts import semantic_scholar
from articles.services import upsert_article


class Command(BaseCommand):
    help = "Fetch articles from Semantic Scholar per biomedical domain."

    def add_arguments(self, parser):
        parser.add_argument("--per-domain", type=int, default=200)
        parser.add_argument("--domain", type=str, default="")

    def handle(self, *args, **opts):
        per = opts["per_domain"]
        only = opts["domain"]
        domains = {only: DOMAINS[only]} if only else DOMAINS

        total_new = 0
        for key, cfg in domains.items():
            self.stdout.write(self.style.NOTICE(
                f"\n[SemanticScholar] '{key}' — {per} articles..."))
            try:
                articles = semantic_scholar.search(cfg["ss_query"], limit=per)
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"  ✗ {e}"))
                continue

            new = 0
            for data in articles:
                _, created = upsert_article(data)
                if created:
                    new += 1
                    total_new += 1
            self.stdout.write(self.style.SUCCESS(
                f"  ✓ {new} nouveaux / {len(articles)} traités"))

        self.stdout.write(self.style.SUCCESS(
            f"\n=== {total_new} nouveaux articles Semantic Scholar ==="))
