"""
Pagination classes for the messaging app.

This module provides pagination configuration for messages
and conversations in the messaging application.
"""
from rest_framework.pagination import PageNumberPagination


class MessagePagination(PageNumberPagination):
    """
    Pagination class for messages.
    
    Fetches 20 messages per page by default.
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class ConversationPagination(PageNumberPagination):
    """
    Pagination class for conversations.
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

