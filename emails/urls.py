from django.urls import path
from . import views

app_name = 'emails'

urlpatterns = [
    path('', views.EmailListView.as_view(), name='list'),
    path('<int:pk>/', views.EmailDetailView.as_view(), name='detail'),
    path('<int:pk>/mark-read/', views.mark_email_read, name='mark_read'),
    path('<int:pk>/mark-unread/', views.mark_email_unread, name='mark_unread'),  # opțional
]