"""
URL patterns for the orders app.

This module defines the URL routing for the orders application, mapping URLs
to their corresponding view functions and classes.
"""

from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('chat/', views.chat_view, name='chat'),
]