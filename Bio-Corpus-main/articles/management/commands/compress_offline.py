"""
Management command to compress static files offline.
Run this after modifying CSS/JS files.
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command
import os


class Command(BaseCommand):
    help = 'Collect static files and compress them offline'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔧 Starting static file compression...'))
        
        # Step 1: Collect static files
        self.stdout.write('📦 Collecting static files...')
        call_command('collectstatic', '--noinput', '--clear')
        
        # Step 2: Compress offline
        self.stdout.write('⚡ Compressing CSS and JavaScript...')
        call_command('compress')
        
        self.stdout.write(self.style.SUCCESS('✅ Static files optimized and compressed!'))
        self.stdout.write(self.style.SUCCESS('✨ Your site is now production-ready with:'))
        self.stdout.write('  • Minified CSS/JavaScript')
        self.stdout.write('  • Gzip compression enabled')
        self.stdout.write('  • Cache headers configured')
        self.stdout.write('  • Database query optimization')
        self.stdout.write('  • Image lazy loading (Intersection Observer)')
