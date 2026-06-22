"""
Management command for importing emails from local folders.

This module defines a Django management command that allows importing email files
(.eml and .msg) from local directories into the database.
"""

from django.core.management.base import BaseCommand
from emails.utils import EmailImporter
import os

class Command(BaseCommand):
    """
    Django management command for importing emails from local folders.
    
    This command provides functionality to import email files from a specified folder
    into the Django database. It supports recursive scanning of subfolders and can
    limit the number of emails imported.
    
    Usage:
        python manage.py import_emails <folder_path> [--recursive] [--limit N]
        
    Examples:
        python manage.py import_emails /path/to/emails/
        python manage.py import_emails /path/to/emails/ --recursive
        python manage.py import_emails /path/to/emails/ --limit 100
        
    Attributes:
        help (str): Description of the command's purpose.
        
    Methods:
        add_arguments: Defines command-line arguments.
        handle: Executes the command logic.
    """
    help = 'Import emails from local folder'

    def add_arguments(self, parser):
        """
        Add command-line arguments to the parser.
        
        Configures the command with required and optional arguments for importing emails.
        
        Args:
            parser (ArgumentParser): The argument parser object to configure.
        """
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
        """
        Execute the command logic.
        
        Processes the command arguments and imports emails from the specified folder.
        
        Args:
            *args: Variable length argument list.
            **options: Arbitrary keyword arguments containing command options.
            
        Returns:
            None
        """
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