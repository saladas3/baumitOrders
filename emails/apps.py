"""
Django app configuration for the emails app.

This module defines the configuration for the emails Django application.
"""

from django.apps import AppConfig


class EmailsConfig(AppConfig):
    """
    Configuration class for the emails app.
    
    This class defines the configuration settings for the emails Django application,
    including the app name and any necessary initialization logic.
    
    Attributes:
        name (str): The name of the Django app.
    """
    name = 'emails'
