# Messaging App - Django Project Configuration

This directory contains the main Django project configuration files for the messaging application.

## Contents

- **`settings.py`** - Main Django settings including:
  - Installed apps configuration
  - Database configuration
  - REST Framework settings
  - **Cache configuration** (LocMemCache with unique-snowflake location)
  - JWT authentication settings

- **`urls.py`** - Root URL configuration:
  - Admin interface routes
  - API routes for chats and messaging apps
  - JWT token endpoints

- **`wsgi.py`** - WSGI configuration for deployment

- **`asgi.py`** - ASGI configuration for async deployment

- **`__init__.py`** - Python package initialization

## Key Configuration

### Cache Settings
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}
```

### Installed Apps
- `chats` - Conversation and message management
- `messaging.apps.MessagingConfig` - Messaging app with signals

## Usage

This is the core Django project configuration. Modify `settings.py` to:
- Add new apps
- Configure databases
- Adjust cache settings
- Modify middleware
- Update security settings

## Notes

- The project uses a custom User model from the `chats` app
- REST Framework is configured with JWT authentication
- Cache is configured for view-level caching

