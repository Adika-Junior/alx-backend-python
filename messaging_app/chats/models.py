import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """Custom User model extending AbstractUser.
    
    Inherits all fields from AbstractUser including:
    - password (hashed password field)
    - username, email, first_name, last_name
    - is_active, is_staff, is_superuser
    - date_joined, last_login
    
    Additional custom fields defined below.
    """
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    first_name = models.CharField(max_length=150, null=False)
    last_name = models.CharField(max_length=150, null=False)
    email = models.EmailField(unique=True, null=False, db_index=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(
        max_length=10,
        choices=[('guest', 'Guest'), ('host', 'Host'), ('admin', 'Admin')],
        null=False,
        default='guest'
    )
    created_at = models.DateTimeField(default=timezone.now)
    
    # Override username to use email
    username = models.CharField(max_length=150, null=True, blank=True, unique=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    class Meta:
        db_table = 'user'
        indexes = [
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


class Conversation(models.Model):
    """Model to track conversations between users."""
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'conversation'
        ordering = ['-created_at']
    
    def __str__(self):
        participant_names = ', '.join([f"{p.first_name} {p.last_name}" for p in self.participants.all()[:3]])
        return f"Conversation {self.conversation_id} - {participant_names}"


class Message(models.Model):
    """Model to store messages in conversations."""
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    message_body = models.TextField(null=False)
    sent_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'message'
        ordering = ['sent_at']
        indexes = [
            models.Index(fields=['conversation', 'sent_at']),
        ]
    
    def __str__(self):
        return f"Message from {self.sender.first_name} at {self.sent_at}"

