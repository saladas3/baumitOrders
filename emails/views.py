"""
Views for the emails app.

This module contains all the view functions and classes for displaying and managing
email data in the Django application.

Classes:
    EmailListView: ListView for displaying a paginated list of emails.
    EmailDetailView: DetailView for displaying individual email details.

Functions:
    mark_email_read: Marks an email as read.
    mark_email_unread: Marks an email as unread.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.db.models import Q
from .models import Email


@method_decorator(login_required, name='dispatch')
class EmailListView(ListView):
    """
    ListView for displaying a paginated list of emails.
    
    This view displays all emails in the database with pagination and search
    functionality. It filters emails based on search queries provided by the user.
    
    Attributes:
        model (Email): The model to use for the view.
        template_name (str): The template to render.
        context_object_name (str): The name of the context variable for the list.
        paginate_by (int): Number of items per page.
        
    Methods:
        get_queryset: Returns the filtered queryset based on search criteria.
    """
    model = Email
    template_name = 'emails/email_list.html'
    context_object_name = 'emails'
    paginate_by = 50

    def get_queryset(self):
        """
        Get the filtered queryset of emails.
        
        Filters emails based on search query provided in GET parameters.
        Search is performed on subject, sender, and body fields.
        
        Args:
            self: The instance of the view.
            
        Returns:
            QuerySet: Filtered queryset of Email objects.
        """
        queryset = super().get_queryset()

        # Filtrare după căutare
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(subject__icontains=search_query) |
                Q(sender__icontains=search_query) |
                Q(body__icontains=search_query)
            )

        return queryset


@method_decorator(login_required, name='dispatch')
class EmailDetailView(DetailView):
    """
    DetailView for displaying individual email details.
    
    This view displays the complete details of a single email message.
    
    Attributes:
        model (Email): The model to use for the view.
        template_name (str): The template to render.
        context_object_name (str): The name of the context variable for the object.
        
    Methods:
        get_object: Returns the email object to display.
    """
    model = Email
    template_name = 'emails/email_detail.html'
    context_object_name = 'email'


@login_required
def mark_email_read(request, pk):
    """
    Mark an email as read.
    
    This view function marks a specific email as read and redirects to the email detail page.
    
    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): Primary key of the email to mark as read.
        
    Returns:
        HttpResponse: Redirects to the email detail page.
        
    Raises:
        Http404: If the email with the given primary key does not exist.
    """
    email = get_object_or_404(Email, pk=pk)
    email.is_read = True
    email.save()
    messages.success(request, f'Email "{email.subject}" marked as read.')
    return redirect('emails:detail', pk=pk)


@login_required
def mark_email_unread(request, pk):
    """
    Mark an email as unread.
    
    This view function marks a specific email as unread and redirects to the email detail page.
    
    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): Primary key of the email to mark as unread.
        
    Returns:
        HttpResponse: Redirects to the email detail page.
        
    Raises:
        Http404: If the email with the given primary key does not exist.
    """
    email = get_object_or_404(Email, pk=pk)
    email.is_read = False
    email.save()
    messages.success(request, f'Email "{email.subject}" marked as unread.')
    return redirect('emails:detail', pk=pk)