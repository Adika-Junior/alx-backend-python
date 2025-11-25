from django.contrib import admin
from .models import Message, Notification, MessageHistory


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Admin interface for Message model."""
    list_display = ('message_id', 'sender', 'receiver', 'content', 'timestamp', 'edited', 'read', 'parent_message')
    list_filter = ('edited', 'read', 'timestamp')
    search_fields = ('content', 'sender__email', 'receiver__email')
    readonly_fields = ('message_id', 'timestamp')
    date_hierarchy = 'timestamp'
    
    fieldsets = (
        ('Message Information', {
            'fields': ('message_id', 'sender', 'receiver', 'content', 'timestamp')
        }),
        ('Status', {
            'fields': ('edited', 'read', 'parent_message')
        }),
    )


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Admin interface for Notification model."""
    list_display = ('notification_id', 'user', 'message', 'content', 'created_at', 'read')
    list_filter = ('read', 'created_at')
    search_fields = ('content', 'user__email')
    readonly_fields = ('notification_id', 'created_at')
    date_hierarchy = 'created_at'


@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    """Admin interface for MessageHistory model."""
    list_display = ('history_id', 'message', 'old_content', 'edited_by', 'edited_at')
    list_filter = ('edited_at', 'edited_by')
    search_fields = ('old_content', 'message__content', 'edited_by__email')
    readonly_fields = ('history_id', 'edited_at')
    date_hierarchy = 'edited_at'

