"""
Custom permission classes for the messaging app.

This module provides permission classes to control access to
conversations and messages based on participant status.
"""
from rest_framework import permissions
from rest_framework.permissions import BasePermission
from .models import Conversation, Message


class IsParticipantOfConversation(BasePermission):
    """
    Custom permission class to check if the user is a participant
    in a conversation.
    
    This permission:
    - Requires authentication
    - Allows only participants in a conversation to send, view, update and delete messages
    - Allows only participants to access conversation details
    """
    
    def has_permission(self, request, view):
        """
        Check if the user is authenticated.
        
        Args:
            request: The request object
            view: The view being accessed
            
        Returns:
            bool: True if user is authenticated, False otherwise
        """
        # Require authentication for all actions
        if not request.user or not request.user.is_authenticated:
            return False
        
        return True
    
    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to access the specific object.
        
        For conversations: User must be a participant
        For messages: User must be a participant in the message's conversation
        Allows only participants to send (POST), view (GET), update (PUT, PATCH), and delete (DELETE) messages
        
        Args:
            request: The request object
            view: The view being accessed
            obj: The object being accessed (Conversation or Message)
            
        Returns:
            bool: True if user has permission, False otherwise
        """
        # Ensure user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Handle Conversation objects
        if isinstance(obj, Conversation):
            return obj.participants.filter(user_id=request.user.user_id).exists()
        
        # Handle Message objects - allow GET, PUT, PATCH, DELETE for participants
        if isinstance(obj, Message):
            conversation = obj.conversation
            # Check if user is a participant in the conversation
            # Allow PUT, PATCH, DELETE only for participants
            is_participant = conversation.participants.filter(user_id=request.user.user_id).exists()
            
            # For PUT, PATCH, DELETE methods, require participant status
            if request.method in ['PUT', 'PATCH', 'DELETE']:
                return is_participant
            
            # For GET (view), also require participant status
            return is_participant
        
        # For other object types, deny by default
        return False


class IsMessageSenderOrParticipant(BasePermission):
    """
    Permission class that allows access if:
    - User is the sender of the message, OR
    - User is a participant in the message's conversation
    """
    
    def has_permission(self, request, view):
        """Require authentication."""
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """Check if user is sender or participant."""
        if not request.user or not request.user.is_authenticated:
            return False
        
        if isinstance(obj, Message):
            # Allow if user is the sender
            if obj.sender.user_id == request.user.user_id:
                return True
            
            # Allow if user is a participant in the conversation
            conversation = obj.conversation
            return conversation.participants.filter(user_id=request.user.user_id).exists()
        
        return False

