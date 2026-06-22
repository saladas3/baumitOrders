"""
Django admin configuration for the emails app.

This module registers the Email model with the Django admin interface,
providing a user-friendly interface for managing email data.
"""

from django.contrib import admin
from .models import Email

@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Email model.
    
    This class defines how the Email model appears in the Django admin interface,
    including list display, search fields, and filtering options.
    
    Attributes:
        list_display (list): Fields to display in the list view.
        list_filter (list): Fields to use for filtering in the list view.
        search_fields (list): Fields to search on in the list view.
        date_hierarchy (str): Field to use for date-based hierarchy navigation.
        list_per_page (int): Number of items to display per page.
    """
    list_display = ('subject', 'sender', 'date_received', 'is_read')
    list_filter = ('is_read', 'date_received', 'sender')
    search_fields = ('subject', 'sender', 'body')
    date_hierarchy = 'date_received'
    list_per_page = 50
