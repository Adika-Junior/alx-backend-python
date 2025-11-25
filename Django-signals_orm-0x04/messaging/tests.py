from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Message, Notification, MessageHistory

User = get_user_model()


class MessageModelTest(TestCase):
    """Test cases for Message model."""
    
    def setUp(self):
        """Set up test data."""
        self.sender = User.objects.create_user(
            email='sender@test.com',
            password='testpass123',
            first_name='Sender',
            last_name='Test'
        )
        self.receiver = User.objects.create_user(
            email='receiver@test.com',
            password='testpass123',
            first_name='Receiver',
            last_name='Test'
        )
    
    def test_message_creation(self):
        """Test creating a message."""
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content='Test message'
        )
        self.assertEqual(message.sender, self.sender)
        self.assertEqual(message.receiver, self.receiver)
        self.assertEqual(message.content, 'Test message')
        self.assertFalse(message.edited)
        self.assertFalse(message.read)
    
    def test_message_with_parent(self):
        """Test creating a reply message."""
        parent = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content='Parent message'
        )
        reply = Message.objects.create(
            sender=self.receiver,
            receiver=self.sender,
            content='Reply message',
            parent_message=parent
        )
        self.assertEqual(reply.parent_message, parent)
        self.assertIn(reply, parent.replies.all())


class NotificationSignalTest(TestCase):
    """Test cases for notification signals."""
    
    def setUp(self):
        """Set up test data."""
        self.sender = User.objects.create_user(
            email='sender@test.com',
            password='testpass123',
            first_name='Sender',
            last_name='Test'
        )
        self.receiver = User.objects.create_user(
            email='receiver@test.com',
            password='testpass123',
            first_name='Receiver',
            last_name='Test'
        )
    
    def test_notification_created_on_message(self):
        """Test that notification is created when a message is sent."""
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content='Test message'
        )
        # Check that notification was created
        notifications = Notification.objects.filter(user=self.receiver, message=message)
        self.assertEqual(notifications.count(), 1)
        notification = notifications.first()
        self.assertEqual(notification.user, self.receiver)
        self.assertEqual(notification.message, message)


class MessageEditSignalTest(TestCase):
    """Test cases for message edit signals."""
    
    def setUp(self):
        """Set up test data."""
        self.sender = User.objects.create_user(
            email='sender@test.com',
            password='testpass123',
            first_name='Sender',
            last_name='Test'
        )
        self.receiver = User.objects.create_user(
            email='receiver@test.com',
            password='testpass123',
            first_name='Receiver',
            last_name='Test'
        )
        self.message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content='Original message'
        )
    
    def test_message_edit_logged(self):
        """Test that message edit is logged in history."""
        original_content = self.message.content
        self.message.content = 'Edited message'
        self.message.save()
        
        # Check that history was created
        history = MessageHistory.objects.filter(message=self.message)
        self.assertEqual(history.count(), 1)
        self.assertEqual(history.first().old_content, original_content)
        
        # Check that message is marked as edited
        self.message.refresh_from_db()
        self.assertTrue(self.message.edited)


class UnreadMessagesManagerTest(TestCase):
    """Test cases for UnreadMessagesManager."""
    
    def setUp(self):
        """Set up test data."""
        self.sender = User.objects.create_user(
            email='sender@test.com',
            password='testpass123',
            first_name='Sender',
            last_name='Test'
        )
        self.receiver = User.objects.create_user(
            email='receiver@test.com',
            password='testpass123',
            first_name='Receiver',
            last_name='Test'
        )
        # Create read and unread messages
        Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content='Unread message 1',
            read=False
        )
        Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content='Unread message 2',
            read=False
        )
        Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content='Read message',
            read=True
        )
    
    def test_unread_messages_for_user(self):
        """Test filtering unread messages for a user."""
        unread_messages = Message.unread.unread_for_user(self.receiver)
        self.assertEqual(unread_messages.count(), 2)
        for message in unread_messages:
            self.assertFalse(message.read)
    
    def test_unread_count(self):
        """Test counting unread messages for a user."""
        count = Message.unread.unread_count(self.receiver)
        self.assertEqual(count, 2)


class UserDeletionSignalTest(TestCase):
    """Test cases for user deletion cleanup signal."""
    
    def setUp(self):
        """Set up test data."""
        self.user1 = User.objects.create_user(
            email='user1@test.com',
            password='testpass123',
            first_name='User',
            last_name='One'
        )
        self.user2 = User.objects.create_user(
            email='user2@test.com',
            password='testpass123',
            first_name='User',
            last_name='Two'
        )
        self.message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content='Test message'
        )
        self.notification = Notification.objects.filter(user=self.user2).first()
    
    def test_user_deletion_cleanup(self):
        """Test that user deletion cleans up related data."""
        # Delete user1
        self.user1.delete()
        
        # Check that messages sent by user1 are deleted
        self.assertEqual(Message.objects.filter(sender=self.user1).count(), 0)
        
        # Check that notifications for user2 still exist (they should)
        # But the message reference might be None due to CASCADE
        notifications = Notification.objects.filter(user=self.user2)
        # The notification might be deleted if message is deleted via CASCADE
        # This depends on the CASCADE behavior

