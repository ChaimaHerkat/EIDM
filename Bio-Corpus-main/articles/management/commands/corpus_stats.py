from django.core.management.base import BaseCommand
from articles.models import Article
from fetch_scripts.domains import DOMAINS


class Command(BaseCommand):
    help = "Print corpus statistics by source and domain."

    def handle(self, *args, **opts):
        total = Article.objects.count()
        self.stdout.write(self.style.SUCCESS(f"\n=== CORPUS: {total} articles ===\n"))

        self.stdout.write("Par source:")
        for s in ["pubmed", "pmc", "semantic_scholar"]:
            n = Article.objects(source=s).count()
            self.stdout.write(f"  {s:20s}  {n:>6}")

        self.stdout.write("\nPar domaine:")
        for key, cfg in DOMAINS.items():
            n = Article.objects(domain=key).count()
            self.stdout.write(f"  {cfg['label']:20s}  {n:>6}")
        unclassified = Article.objects(domain="").count()
        self.stdout.write(f"  {'(non classés)':20s}  {unclassified:>6}")
