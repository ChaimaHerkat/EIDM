from django.core.management.base import BaseCommand
from articles.models import Article
from fetch_scripts.classifier import classify


class Command(BaseCommand):
    help = "Re-classify all articles in the corpus by biomedical domain."

    def add_arguments(self, parser):
        parser.add_argument("--only-empty", action="store_true",
                            help="Only classify articles without a domain.")

    def handle(self, *args, **opts):
        qs = Article.objects(domain="") if opts["only_empty"] else Article.objects.all()
        total = qs.count()
        self.stdout.write(f"Classification de {total} articles...")
        updated = 0
        for art in qs:
            d, c = classify(art.title, art.abstract, art.mesh_terms, art.keywords)
            if d:
                art.domain = d
                art.domain_confidence = c
                art.save()
                updated += 1
        self.stdout.write(self.style.SUCCESS(
            f"✓ {updated} articles classifiés."))
