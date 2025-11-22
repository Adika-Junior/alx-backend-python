from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Conversation, Message, User
from .serializers import (
    ConversationSerializer,
    ConversationListSerializer,
    MessageSerializer
)
from .permissions import IsParticipantOfConversation
from .pagination import MessagePagination, ConversationPagination
from .filters import MessageFilter, ConversationFilter


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing conversations.
    
    list: Get all conversations
    retrieve: Get a specific conversation with all messages
    create: Create a new conversation
    update: Update a conversation
    destroy: Delete a conversation
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsParticipantOfConversation]
    pagination_class = ConversationPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ConversationFilter
    search_fields = ['participants__email', 'participants__first_name', 'participants__last_name']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Use different serializers for list and detail views."""
        if self.action == 'list':
            return ConversationListSerializer
        return ConversationSerializer
    
    def get_queryset(self):
        """Filter conversations to only show those where the user is a participant."""
        queryset = Conversation.objects.all()
        
        # Only show conversations where the authenticated user is a participant
        if self.request.user and self.request.user.is_authenticated:
            queryset = queryset.filter(participants__user_id=self.request.user.user_id).distinct()
        
        return queryset.prefetch_related('participants', 'messages__sender')
    
    def create(self, request, *args, **kwargs):
        """Create a new conversation with participants."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @action(detail=True, methods=['post'])
    def add_participant(self, request, pk=None):
        """Add a participant to a conversation."""
        conversation = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response(
                {'error': 'user_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(user_id=user_id)
            conversation.participants.add(user)
            serializer = self.get_serializer(conversation)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing messages.
    
    list: Get all messages (optionally filtered by conversation)
    retrieve: Get a specific message
    create: Send a new message to a conversation
    update: Update a message
    destroy: Delete a message
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MessageFilter
    search_fields = ['message_body', 'sender__email', 'sender__first_name', 'sender__last_name']
    ordering_fields = ['sent_at', 'created_at']
    ordering = ['-sent_at']
    
    def get_queryset(self):
        """Filter messages by conversation if provided via nested route or query param.
        Only show messages from conversations where the user is a participant.
        """
        queryset = Message.objects.select_related('sender', 'conversation')
        
        # Only show messages from conversations where the authenticated user is a participant
        if self.request.user and self.request.user.is_authenticated:
            queryset = queryset.filter(
                conversation__participants__user_id=self.request.user.user_id
            ).distinct()
        
        # Handle nested route: conversations/{id}/messages/
        conversation_pk = self.kwargs.get('conversation_pk', None)
        if conversation_pk:
            queryset = queryset.filter(conversation__conversation_id=conversation_pk)
        else:
            # Handle query parameter for top-level messages endpoint
            conversation_id = self.request.query_params.get('conversation', None)
            if conversation_id:
                queryset = queryset.filter(conversation__conversation_id=conversation_id)
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        """Create a new message in a conversation."""
        data = request.data.copy()
        
        # Handle nested route: automatically set conversation from URL
        conversation_pk = self.kwargs.get('conversation_pk', None)
        if conversation_pk:
            try:
                conversation = Conversation.objects.get(conversation_id=conversation_pk)
                # Verify user is a participant
                if not conversation.participants.filter(user_id=request.user.user_id).exists():
                    return Response(
                        {'error': 'You are not a participant in this conversation'},
                        status=status.HTTP_403_FORBIDDEN
                    )
                data['conversation'] = conversation.conversation_id
            except Conversation.DoesNotExist:
                return Response(
                    {'error': 'Conversation not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        # Set sender from request user (always use authenticated user)
        if request.user and request.user.is_authenticated:
            data['sender_id'] = request.user.user_id
        else:
            return Response(
                {'error': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Validate conversation access if conversation is provided in data
        if 'conversation' in data and conversation_pk is None:
            try:
                conversation = Conversation.objects.get(conversation_id=data['conversation'])
                if not conversation.participants.filter(user_id=request.user.user_id).exists():
                    return Response(
                        {'error': 'You are not a participant in this conversation'},
                        status=status.HTTP_403_FORBIDDEN
                    )
            except Conversation.DoesNotExist:
                return Response(
                    {'error': 'Conversation not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

