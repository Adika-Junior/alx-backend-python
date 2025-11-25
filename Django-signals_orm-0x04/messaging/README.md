# Messaging App

This Django app implements a messaging system with Django Signals, advanced ORM techniques, and caching.

## Overview

The messaging app provides:
- Direct messaging between users
- Automatic notifications via signals
- Message edit history tracking
- Threaded conversations (replies)
- Unread message filtering
- User account deletion with data cleanup

## Models

### Message
Stores messages between users with the following fields:
- `message_id` (UUID, Primary Key)
- `sender` (ForeignKey to User)
- `receiver` (ForeignKey to User)
- `content` (TextField)
- `timestamp` (DateTimeField)
- `edited` (BooleanField) - Tracks if message was edited
- `read` (BooleanField) - Tracks if message was read
- `parent_message` (Self-referential ForeignKey) - For threaded replies

**Custom Manager**: `UnreadMessagesManager`
- `Message.unread.unread_for_user(user)` - Get unread messages for a user
- `Message.unread.unread_count(user)` - Count unread messages

### Notification
Stores notifications for users:
- `notification_id` (UUID, Primary Key)
- `user` (ForeignKey to User)
- `message` (ForeignKey to Message, nullable)
- `content` (TextField)
- `created_at` (DateTimeField)
- `read` (BooleanField)

### MessageHistory
Stores edit history for messages:
- `history_id` (UUID, Primary Key)
- `message` (ForeignKey to Message)
- `old_content` (TextField) - Previous content before edit
- `edited_at` (DateTimeField)

## Signals

### `post_save` on Message
**File**: `signals.py`
- Automatically creates a notification when a new message is created
- Only notifies the receiver (not the sender)

### `pre_save` on Message
**File**: `signals.py`
- Logs the old content to `MessageHistory` before updating
- Marks the message as `edited=True` when content changes

### `post_delete` on User
**File**: `signals.py`
- Cleans up all messages sent or received by the deleted user
- Deletes all notifications for the user
- MessageHistory is automatically deleted via CASCADE

## Views

### MessageViewSet
**File**: `views.py`

**Endpoints**:
- `GET /api/messaging/messages/` - List messages (cached for 60 seconds)
  - Uses `select_related()` and `prefetch_related()` for optimization
  - Returns threaded conversation structure
  - Uses `.only()` to limit field retrieval
  
- `GET /api/messaging/messages/unread/` - Get unread messages
  - Uses custom `UnreadMessagesManager`
  - Optimized with `.only()` to fetch only necessary fields

- `GET /api/messaging/messages/{id}/history/` - Get message edit history
  - Returns all previous versions of a message

### delete_user
**File**: `views.py`
- `POST /api/messaging/delete-user/` - Delete authenticated user's account
- Triggers `post_delete` signal for automatic cleanup

## Query Optimization

The views use several ORM optimization techniques:

1. **select_related()**: For foreign key relationships (sender, receiver, parent_message)
2. **prefetch_related()**: For reverse foreign keys (replies)
3. **only()**: To limit field retrieval and reduce memory usage
4. **Prefetch objects**: For nested prefetching of replies

## Caching

The message list view is cached for 60 seconds using `@cache_page(60)` decorator.

## Admin Interface

All models are registered in `admin.py` with:
- List displays
- Search fields
- Filters
- Read-only fields for IDs and timestamps

## Testing

Test cases are provided in `tests.py`:
- Message model tests
- Notification signal tests
- Message edit signal tests
- UnreadMessagesManager tests
- User deletion signal tests

Run tests with:
```bash
python manage.py test messaging
```

## Files

- `models.py` - All model definitions
- `signals.py` - Signal handlers
- `views.py` - API views with optimizations
- `urls.py` - URL routing
- `admin.py` - Admin interface configuration
- `apps.py` - App configuration (loads signals)
- `tests.py` - Test cases

## Usage Example

```python
from messaging.models import Message
from django.contrib.auth import get_user_model

User = get_user_model()

# Get unread messages for a user
unread = Message.unread.unread_for_user(user)

# Create a message (triggers notification signal)
message = Message.objects.create(
    sender=user1,
    receiver=user2,
    content="Hello!"
)

# Edit a message (triggers edit history signal)
message.content = "Hello, updated!"
message.save()  # Creates MessageHistory entry

# Get edit history
history = message.history.all()
```

