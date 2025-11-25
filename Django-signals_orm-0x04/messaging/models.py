import uuid
from django.db import models
from django.utils import timezone
from django.conf import settings
from .managers import UnreadMessagesManager


class Message(models.Model):
    """Model to store messages between users."""
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        db_index=True
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_messages',
        db_index=True
    )
    content = models.TextField(null=False)
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    edited = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    parent_message = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='replies',
        null=True,
        blank=True
    )
    
    # Custom manager
    unread = UnreadMessagesManager()
    objects = models.Manager()
    
    class Meta:
        db_table = 'messaging_message'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['receiver', 'read', '-timestamp']),
            models.Index(fields=['sender', '-timestamp']),
            models.Index(fields=['parent_message']),
        ]
    
    def __str__(self):
        return f"Message from {self.sender.email} to {self.receiver.email} at {self.timestamp}"


class Notification(models.Model):
    """Model to store notifications for users."""
    notification_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        db_index=True
    )
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='notifications',
        null=True,
        blank=True
    )
    content = models.TextField(null=False)
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    read = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'messaging_notification'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'read', '-created_at']),
        ]
    
    def __str__(self):
        return f"Notification for {self.user.email} at {self.created_at}"


class MessageHistory(models.Model):
    """Model to store message edit history."""
    history_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name='history',
        db_index=True
    )
    old_content = models.TextField(null=False)
    edited_at = models.DateTimeField(default=timezone.now, db_index=True)
    edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='message_edits',
        db_index=True,
        null=True,
        blank=True
    )
    
    class Meta:
        db_table = 'messaging_messagehistory'
        ordering = ['-edited_at']
        indexes = [
            models.Index(fields=['message', '-edited_at']),
            models.Index(fields=['edited_by', '-edited_at']),
        ]
    
    def __str__(self):
        return f"History for message {self.message.message_id} at {self.edited_at}"

