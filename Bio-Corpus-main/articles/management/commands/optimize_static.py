"""
Management command to optimize and collect static files with compression
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings


class Command(BaseCommand):
    help = "Collect and compress static files for production"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("🚀 Starting static files optimization..."))

        try:
            # Collect static files
            self.stdout.write(self.style.HTTP_INFO("📦 Collecting static files..."))
            call_command("collectstatic", "--noinput", "--clear")
            self.stdout.write(self.style.SUCCESS("✅ Static files collected"))

            # Compress static files
            self.stdout.write(self.style.HTTP_INFO("🗜️  Compressing static files..."))
            call_command("compress", "--force")
            self.stdout.write(self.style.SUCCESS("✅ Static files compressed"))

            self.stdout.write(self.style.SUCCESS("\n✨ Optimization complete!"))
            self.stdout.write(f"📁 Static root: {settings.STATIC_ROOT}")

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error: {str(e)}"))
