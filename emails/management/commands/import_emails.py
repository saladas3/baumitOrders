from django.core.management.base import BaseCommand
from emails.utils import EmailImporter
import os

class Command(BaseCommand):
    help = 'Import emails from local folder'

    def add_arguments(self, parser):
        parser.add_argument(
            'folder_path',
            type=str,
            help='Path to folder containing email files'
        )
        parser.add_argument(
            '--recursive',
            action='store_true',
            help='Recursively scan subfolders'
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=0,
            help='Limit number of emails to import'
        )

    def handle(self, *args, **options):
        folder_path = options['folder_path']
        recursive = options['recursive']
        limit = options['limit']

        if not os.path.exists(folder_path):
            self.stderr.write(self.style.ERROR(f'Folder not found: {folder_path}'))
            return

        self.stdout.write(self.style.SUCCESS(f'Starting import from: {folder_path}'))

        result = EmailImporter.import_from_folder(folder_path, recursive)

        self.stdout.write(self.style.SUCCESS(
            f"\nImport completed:\n"
            f"  - Imported: {result['imported']}\n"
            f"  - Skipped (already exists): {result['skipped']}\n"
            f"  - Errors: {result['errors']}"
        ))

        if result['error_details']:
            self.stderr.write(self.style.ERROR("\nErrors:"))
            for error in result['error_details'][:10]:  # Show first 10 errors
                self.stderr.write(f"  - {error}")