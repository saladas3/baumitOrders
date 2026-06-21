from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone


class Email(models.Model):
    subject = models.CharField(max_length=500, blank=True, null=True)
    sender = models.EmailField(max_length=255, blank=True, null=True)
    receiver = models.EmailField(max_length=255, blank=True, null=True)
    date_sent = models.DateTimeField(blank=True, null=True)
    date_received = models.DateTimeField(blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    body_html = models.TextField(blank=True, null=True)
    attachments = models.JSONField(default=list, blank=True)
    message_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    folder_path = models.CharField(max_length=500, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_received', '-date_sent']
        indexes = [
            models.Index(fields=['sender']),
            models.Index(fields=['date_received']),
        ]

    def __str__(self):
        return f"{self.subject or 'No Subject'} - {self.sender or 'Unknown Sender'}"