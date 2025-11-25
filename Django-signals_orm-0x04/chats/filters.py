"""
Filter classes for the messaging app.

This module provides filtering capabilities using django-filters
to retrieve conversations with specific users or messages within a time range.
"""
import django_filters
from django_filters import rest_framework as filters
from .models import Message, Conversation
from django.contrib.auth import get_user_model

User = get_user_model()


class MessageFilter(filters.FilterSet):
    """
    Filter class for messages.
    
    Allows filtering by:
    - conversation: Filter messages by conversation ID
    - sender: Filter messages by sender user ID or email
    - sent_at: Filter messages by sent date/time range
    - conversation_participant: Filter messages by conversations where a specific user is a participant
    """
    
    # Filter by conversation
    conversation = filters.UUIDFilter(field_name='conversation__conversation_id')
    
    # Filter by sender (by user_id or email)
    sender = filters.UUIDFilter(field_name='sender__user_id')
    sender_email = filters.CharFilter(field_name='sender__email', lookup_expr='iexact')
    
    # Filter by date range
    sent_at_after = filters.DateTimeFilter(field_name='sent_at', lookup_expr='gte')
    sent_at_before = filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')
    sent_at = filters.DateFilter(field_name='sent_at', lookup_expr='date')
    
    # Filter by conversation participant
    conversation_participant = filters.UUIDFilter(
        field_name='conversation__participants__user_id',
        distinct=True
    )
    conversation_participant_email = filters.CharFilter(
        field_name='conversation__participants__email',
        lookup_expr='iexact',
        distinct=True
    )
    
    class Meta:
        model = Message
        fields = ['conversation', 'sender', 'sender_email', 'sent_at', 
                  'sent_at_after', 'sent_at_before', 'conversation_participant',
                  'conversation_participant_email']


class ConversationFilter(filters.FilterSet):
    """
    Filter class for conversations.
    
    Allows filtering by:
    - participant: Filter conversations by participant user ID or email
    - created_at: Filter conversations by creation date/time range
    """
    
    # Filter by participant
    participant = filters.UUIDFilter(
        field_name='participants__user_id',
        distinct=True
    )
    participant_email = filters.CharFilter(
        field_name='participants__email',
        lookup_expr='iexact',
        distinct=True
    )
    
    # Filter by date range
    created_at_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_at_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    created_at = filters.DateFilter(field_name='created_at', lookup_expr='date')
    
    class Meta:
        model = Conversation
        fields = ['participant', 'participant_email', 'created_at',
                  'created_at_after', 'created_at_before']

