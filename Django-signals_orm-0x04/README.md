# Django Signals, ORM, and Caching Project

This project demonstrates advanced Django concepts including Signals, ORM optimization techniques, and basic caching strategies.

## Project Overview

This Django application implements a messaging system with the following features:
- Event-driven notifications using Django Signals
- Optimized database queries using advanced ORM techniques
- Threaded conversations with efficient query patterns
- Custom managers for filtering unread messages
- View-level caching for improved performance

## Project Structure

```
Django-signals_orm-0x04/
├── messaging_app/          # Main Django project configuration
├── chats/                  # Chat/conversation app (existing)
├── messaging/              # Messaging app with signals and advanced ORM
├── manage.py               # Django management script
└── requirements.txt        # Python dependencies
```

## Features Implemented

### 1. Django Signals
- **post_save signal**: Automatically creates notifications when new messages are sent
- **pre_save signal**: Logs message edit history before updates
- **post_delete signal**: Cleans up user-related data when accounts are deleted

### 2. Advanced ORM Techniques
- **select_related()**: Optimizes foreign key queries
- **prefetch_related()**: Optimizes reverse foreign key and many-to-many queries
- **Custom Manager**: `UnreadMessagesManager` for filtering unread messages
- **Threaded Conversations**: Self-referential foreign keys with recursive queries

### 3. Caching
- **LocMemCache**: In-memory caching backend configured
- **View-level caching**: 60-second cache on message list views

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

3. Create a superuser:
```bash
python manage.py createsuperuser
```

4. Run the development server:
```bash
python manage.py runserver
```

## API Endpoints

### Messaging App
- `GET /api/messaging/messages/` - List messages (cached for 60 seconds)
- `POST /api/messaging/messages/` - Create a new message
- `GET /api/messaging/messages/{id}/` - Retrieve a message
- `GET /api/messaging/messages/unread/` - Get unread messages
- `GET /api/messaging/messages/{id}/history/` - Get message edit history
- `POST /api/messaging/delete-user/` - Delete user account

### Chats App
- `GET /api/conversations/` - List conversations
- `GET /api/conversations/{id}/messages/` - List messages in conversation (cached for 60 seconds)

## Testing

Run the test suite:
```bash
python manage.py test messaging
```

## Key Files

- `messaging/models.py` - Message, Notification, and MessageHistory models
- `messaging/signals.py` - Signal handlers for notifications, edits, and cleanup
- `messaging/views.py` - ViewSet with optimized queries and caching
- `messaging_app/settings.py` - Cache configuration
- `chats/views.py` - Cached message list view

## Technologies Used

- Django 4.2
- Django REST Framework
- Django Signals
- LocMemCache

## Author

ALX Backend Python Project

