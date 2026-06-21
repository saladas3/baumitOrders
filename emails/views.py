from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.db.models import Q
from .models import Email


@method_decorator(login_required, name='dispatch')
class EmailListView(ListView):
    model = Email
    template_name = 'emails/email_list.html'
    context_object_name = 'emails'
    paginate_by = 50

    def get_queryset(self):
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
    model = Email
    template_name = 'emails/email_detail.html'
    context_object_name = 'email'


@login_required
def mark_email_read(request, pk):
    """Marchează emailul ca citit"""
    email = get_object_or_404(Email, pk=pk)
    email.is_read = True
    email.save()
    messages.success(request, f'Email "{email.subject}" marked as read.')
    return redirect('emails:detail', pk=pk)


@login_required
def mark_email_unread(request, pk):
    """Marchează emailul ca necitit"""
    email = get_object_or_404(Email, pk=pk)
    email.is_read = False
    email.save()
    messages.success(request, f'Email "{email.subject}" marked as unread.')
    return redirect('emails:detail', pk=pk)