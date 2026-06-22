"""
Email model for storing email data.

This module defines the Email model which represents email messages in the database.
It includes fields for subject, sender, receiver, dates, body content, attachments,
and other email metadata.

Classes:
    Email: Model representing an email message with various attributes and methods.
"""

from django.db import models
from django.utils import timezone


class Email(models.Model):
    """
    Model representing an email message.

    This model stores all relevant information about email messages including
    subject, sender, receiver, dates, content, attachments, and metadata.

    Attributes:
        subject (CharField): The subject line of the email (max 500 characters).
        sender (EmailField): The email address of the sender.
        receiver (EmailField): The email address of the receiver.
        date_sent (DateTimeField): The date and time when the email was sent.
        date_received (DateTimeField): The date and time when the email was received.
        body (TextField): The plain text content of the email body.
        body_html (TextField): The HTML content of the email body.
        attachments (JSONField): List of attachment information in JSON format.
        message_id (CharField): Unique identifier for the email message.
        folder_path (CharField): Path to the folder where the email is stored.
        is_read (BooleanField): Flag indicating if the email has been read.
        created_at (DateTimeField): Timestamp when the email record was created.

    Meta:
        ordering: Emails are ordered by date received and sent (newest first).
        indexes: Database indexes on sender and date_received fields for performance.
    """
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
        """
        Meta options for the Email model.
        
        Defines ordering and database indexes for optimal performance.
        """
        ordering = ['-date_received', '-date_sent']
        indexes = [
            models.Index(fields=['sender']),
            models.Index(fields=['date_received']),
        ]

    def __str__(self):
        """
        String representation of the Email object.
        
        Returns:
            str: A formatted string showing subject and sender, or default values
                 if they are not set.
        """
        return f"{self.subject or 'No Subject'} - {self.sender or 'Unknown Sender'}"