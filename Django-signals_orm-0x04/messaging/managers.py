from django.db import models


class UnreadMessagesManager(models.Manager):
    """Custom manager to filter unread messages for a specific user."""
    
    def unread_for_user(self, user):
        """Return unread messages for a specific user."""
        return self.filter(receiver=user, read=False)
    
    def unread_count(self, user):
        """Return count of unread messages for a specific user."""
        return self.filter(receiver=user, read=False).count()

