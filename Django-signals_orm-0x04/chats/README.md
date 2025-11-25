# Chats App

This Django app handles conversations and messages between users using the conversation-based model.

## Overview

The chats app provides:
- Multi-participant conversations
- Messages within conversations
- User authentication and management
- RESTful API endpoints
- Cached message list views

## Models

### User
Custom user model extending `AbstractUser`:
- `user_id` (UUID, Primary Key)
- `email` (EmailField, unique)
- `first_name`, `last_name` (CharField)
- `phone_number` (CharField, optional)
- `role` (CharField with choices: guest, host, admin)
- `created_at` (DateTimeField)

### Conversation
Tracks conversations between multiple users:
- `conversation_id` (UUID, Primary Key)
- `participants` (ManyToManyField to User)
- `created_at` (DateTimeField)

### Message
Messages within conversations:
- `message_id` (UUID, Primary Key)
- `sender` (ForeignKey to User)
- `conversation` (ForeignKey to Conversation)
- `message_body` (TextField)
- `sent_at` (DateTimeField)

## Views

### ConversationViewSet
**File**: `views.py`

**Endpoints**:
- `GET /api/conversations/` - List user's conversations
- `GET /api/conversations/{id}/` - Get conversation details
- `POST /api/conversations/` - Create a new conversation
- `POST /api/conversations/{id}/add_participant/` - Add participant

**Features**:
- Filters conversations to show only those where user is a participant
- Uses `prefetch_related()` for optimization

### MessageViewSet
**File**: `views.py`

**Endpoints**:
- `GET /api/conversations/{id}/messages/` - List messages in conversation
  - **Cached for 60 seconds** using `@cache_page(60)`
- `POST /api/conversations/{id}/messages/` - Send a message
- `GET /api/messages/` - List all messages (with conversation filter)
- `GET /api/messages/{id}/` - Get message details

**Features**:
- Only shows messages from conversations where user is a participant
- Uses `select_related()` for sender and conversation
- Uses `prefetch_related()` for conversation participants
- Cached list view for performance

## Query Optimization

The views use ORM optimization techniques:

1. **select_related()**: For foreign key relationships
   ```python
   .select_related('sender', 'conversation')
   ```

2. **prefetch_related()**: For many-to-many and reverse relationships
   ```python
   .prefetch_related('participants', 'messages__sender')
   ```

3. **distinct()**: To avoid duplicate results in filtered queries

## Caching

The message list view (`list` method) is cached for 60 seconds:
```python
@method_decorator(cache_page(60))
def list(self, request, *args, **kwargs):
    return super().list(request, *args, **kwargs)
```

This reduces database load for frequently accessed conversation messages.

## Permissions

- `IsAuthenticated`: All endpoints require authentication
- `IsParticipantOfConversation`: Users can only access conversations they're part of

## Serializers

- `ConversationSerializer`: Full conversation details with messages
- `ConversationListSerializer`: Lightweight list view
- `MessageSerializer`: Message representation

## Filters

- `ConversationFilter`: Filter conversations by participants
- `MessageFilter`: Filter messages by conversation, sender, etc.

## Pagination

- `ConversationPagination`: Paginates conversation lists
- `MessagePagination`: Paginates message lists

## Files

- `models.py` - User, Conversation, and Message models
- `views.py` - ViewSets with caching
- `serializers.py` - DRF serializers
- `urls.py` - URL routing
- `permissions.py` - Custom permission classes
- `filters.py` - Filter classes
- `pagination.py` - Pagination classes
- `auth.py` - Custom JWT authentication
- `admin.py` - Admin interface (if configured)
- `tests.py` - Test cases

## API Usage

### Create a Conversation
```bash
POST /api/conversations/
{
    "participants": ["user_id_1", "user_id_2"]
}
```

### Send a Message
```bash
POST /api/conversations/{conversation_id}/messages/
{
    "message_body": "Hello, everyone!"
}
```

### Get Messages (Cached)
```bash
GET /api/conversations/{conversation_id}/messages/
```

## Notes

- Messages are cached at the view level for 60 seconds
- All queries are optimized to minimize database hits
- Users can only see conversations they participate in
- The app uses JWT authentication for API access

