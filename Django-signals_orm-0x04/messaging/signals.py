from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from .models import Message, Notification, MessageHistory


@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance, created, **kwargs):
    """Create a notification when a new message is created."""
    if created:
        # Only create notification for the receiver (not the sender)
        if instance.receiver != instance.sender:
            Notification.objects.create(
                user=instance.receiver,
                message=instance,
                content=f"You received a new message from {instance.sender.first_name} {instance.sender.last_name}: {instance.content[:50]}..."
            )


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """Log the old content of a message before it's updated."""
    if instance.pk:  # Only for existing messages (updates, not creates)
        try:
            old_message = Message.objects.get(pk=instance.pk)
            # Check if content has changed
            if old_message.content != instance.content:
                # Save the old content to history with edited_by (typically the sender)
                # The sender is the one who can edit their own message
                MessageHistory.objects.create(
                    message=old_message,
                    old_content=old_message.content,
                    edited_by=instance.sender
                )
                # Mark message as edited
                instance.edited = True
        except Message.DoesNotExist:
            pass


@receiver(post_delete, sender=settings.AUTH_USER_MODEL)
def cleanup_user_data(sender, instance, **kwargs):
    """Clean up all messages, notifications, and message histories when a user is deleted.
    
    Note: Most deletions happen automatically via CASCADE, but this signal ensures
    complete cleanup and handles any edge cases.
    """
    # Delete all messages sent or received by the user
    # (These should be deleted via CASCADE, but we ensure cleanup)
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    
    # Delete all notifications for the user
    # (These should be deleted via CASCADE, but we ensure cleanup)
    Notification.objects.filter(user=instance).delete()
    
    # Note: MessageHistory will be automatically deleted via CASCADE
    # when the associated Message is deleted

