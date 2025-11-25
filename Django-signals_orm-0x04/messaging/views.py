from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.db.models import Q, Prefetch
from django.contrib.auth import get_user_model
from .models import Message, Notification, MessageHistory

User = get_user_model()


class MessageViewSet(viewsets.ModelViewSet):
    """ViewSet for managing messages with optimized queries."""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Get messages for the authenticated user with optimized queries."""
        # Use select_related for foreign keys and prefetch_related for reverse relations
        # Optimize querying of messages and their replies, reducing the number of database queries
        queryset = Message.objects.filter(
            Q(sender=self.request.user) | Q(receiver=self.request.user)
        ).select_related(
            'sender',
            'receiver',
            'parent_message'
        ).prefetch_related(
            'replies__sender',
            'replies__receiver',
            Prefetch(
                'replies',
                queryset=Message.objects.select_related('sender', 'receiver').prefetch_related('replies')
            )
        ).only(
            'message_id',
            'sender__user_id',
            'sender__email',
            'sender__first_name',
            'sender__last_name',
            'receiver__user_id',
            'receiver__email',
            'receiver__first_name',
            'receiver__last_name',
            'content',
            'timestamp',
            'edited',
            'read',
            'parent_message__message_id',
            'parent_message__content'
        )
        
        return queryset
    
    @method_decorator(cache_page(60))
    def list(self, request, *args, **kwargs):
        """List messages in a conversation with caching."""
        conversation_id = request.query_params.get('conversation', None)
        user = request.user
        
        # Use prefetch_related and select_related to optimize querying of messages and their replies
        if conversation_id:
            # For conversation-based messages (using chats app)
            queryset = self.get_queryset().filter(conversation__conversation_id=conversation_id)
        else:
            # For direct messages - optimize with select_related and prefetch_related
            other_user_id = request.query_params.get('user', None)
            if other_user_id:
                try:
                    other_user = User.objects.get(user_id=other_user_id)
                    queryset = Message.objects.filter(
                        Q(sender=request.user, receiver=other_user) | Q(sender=other_user, receiver=request.user)
                    ).select_related('sender', 'receiver', 'parent_message').prefetch_related(
                        'replies__sender',
                        'replies__receiver',
                        Prefetch(
                            'replies',
                            queryset=Message.objects.select_related('sender', 'receiver').prefetch_related('replies')
                        )
                    )
                except User.DoesNotExist:
                    return Response(
                        {'error': 'User not found'},
                        status=status.HTTP_404_NOT_FOUND
                    )
            else:
                # Filter messages where sender=request.user or receiver=request.user with optimizations
                queryset = Message.objects.filter(
                    Q(sender=request.user) | Q(receiver=request.user)
                ).select_related('sender', 'receiver', 'parent_message').prefetch_related(
                    'replies__sender',
                    'replies__receiver',
                    Prefetch(
                        'replies',
                        queryset=Message.objects.select_related('sender', 'receiver').prefetch_related('replies')
                    )
                )
        
        # Get all messages and their replies in a threaded format
        messages = list(queryset.filter(parent_message__isnull=True))
        
        # Build threaded structure
        result = []
        for message in messages:
            message_data = {
                'message_id': str(message.message_id),
                'sender': {
                    'user_id': str(message.sender.user_id),
                    'email': message.sender.email,
                    'first_name': message.sender.first_name,
                    'last_name': message.sender.last_name,
                },
                'receiver': {
                    'user_id': str(message.receiver.user_id),
                    'email': message.receiver.email,
                    'first_name': message.receiver.first_name,
                    'last_name': message.receiver.last_name,
                },
                'content': message.content,
                'timestamp': message.timestamp,
                'edited': message.edited,
                'read': message.read,
                'replies': self._get_replies(message)
            }
            result.append(message_data)
        
        return Response(result)
    
    def _get_replies(self, message):
        """Recursively get all replies to a message."""
        replies = []
        for reply in message.replies.all():
            reply_data = {
                'message_id': str(reply.message_id),
                'sender': {
                    'user_id': str(reply.sender.user_id),
                    'email': reply.sender.email,
                    'first_name': reply.sender.first_name,
                    'last_name': reply.sender.last_name,
                },
                'receiver': {
                    'user_id': str(reply.receiver.user_id),
                    'email': reply.receiver.email,
                    'first_name': reply.receiver.first_name,
                    'last_name': reply.receiver.last_name,
                },
                'content': reply.content,
                'timestamp': reply.timestamp,
                'edited': reply.edited,
                'read': reply.read,
                'replies': self._get_replies(reply)
            }
            replies.append(reply_data)
        return replies
    
    @action(detail=False, methods=['get'])
    def unread(self, request):
        """Get unread messages for the authenticated user."""
        user = request.user
        unread_messages = Message.unread.unread_for_user(user).only(
            'message_id',
            'sender__user_id',
            'sender__email',
            'sender__first_name',
            'sender__last_name',
            'content',
            'timestamp'
        )
        
        result = []
        for message in unread_messages:
            result.append({
                'message_id': str(message.message_id),
                'sender': {
                    'user_id': str(message.sender.user_id),
                    'email': message.sender.email,
                    'first_name': message.sender.first_name,
                    'last_name': message.sender.last_name,
                },
                'content': message.content,
                'timestamp': message.timestamp,
            })
        
        return Response(result)
    
    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        """Get edit history for a message - display previous versions of messages."""
        message = self.get_object()
        # Display the message edit history in the user interface
        history = MessageHistory.objects.filter(message=message).select_related('edited_by').order_by('-edited_at')
        
        result = []
        for entry in history:
            result.append({
                'history_id': str(entry.history_id),
                'old_content': entry.old_content,
                'edited_at': entry.edited_at,
                'edited_by': {
                    'user_id': str(entry.edited_by.user_id) if entry.edited_by else None,
                    'email': entry.edited_by.email if entry.edited_by else None,
                    'first_name': entry.edited_by.first_name if entry.edited_by else None,
                    'last_name': entry.edited_by.last_name if entry.edited_by else None,
                } if entry.edited_by else None,
            })
        
        return Response(result)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    """Delete the authenticated user's account."""
    user = request.user
    
    # The post_delete signal will automatically clean up:
    # - All messages sent or received by the user
    # - All notifications for the user
    # - All message histories (via CASCADE)
    
    # Delete the user (this will trigger the post_delete signal)
    user.delete()
    
    return Response(
        {'message': 'User account and all related data have been deleted successfully'},
        status=status.HTTP_200_OK
    )

