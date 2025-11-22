from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'created_at']
        read_only_fields = ['user_id', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model."""
    sender = UserSerializer(read_only=True)
    sender_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='sender',
        write_only=True,
        required=False
    )
    conversation = serializers.PrimaryKeyRelatedField(queryset=Conversation.objects.all())
    message_body = serializers.CharField(required=True, allow_blank=False, max_length=5000)
    
    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'sender_id', 'conversation', 'message_body', 'sent_at']
        read_only_fields = ['message_id', 'sent_at']
    
    def validate_message_body(self, value):
        """Validate message body is not empty."""
        if not value or not value.strip():
            raise serializers.ValidationError("Message body cannot be empty.")
        return value.strip()
    
    def create(self, validated_data):
        """Create a new message."""
        return Message.objects.create(**validated_data)


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for Conversation model with nested messages."""
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'participant_ids', 'messages', 'created_at']
        read_only_fields = ['conversation_id', 'created_at']
    
    def validate_participant_ids(self, value):
        """Validate participant IDs."""
        if value and len(value) < 2:
            raise serializers.ValidationError("A conversation must have at least 2 participants.")
        if value:
            # Check if all participant IDs exist
            existing_ids = set(User.objects.filter(user_id__in=value).values_list('user_id', flat=True))
            provided_ids = set(value)
            missing_ids = provided_ids - existing_ids
            if missing_ids:
                raise serializers.ValidationError(f"Invalid participant IDs: {list(missing_ids)}")
        return value
    
    def create(self, validated_data):
        """Create a new conversation with participants."""
        participant_ids = validated_data.pop('participant_ids', [])
        conversation = Conversation.objects.create(**validated_data)
        
        # Add participants
        if participant_ids:
            participants = User.objects.filter(user_id__in=participant_ids)
            conversation.participants.set(participants)
        
        return conversation
    
    def update(self, instance, validated_data):
        """Update conversation, including participants."""
        participant_ids = validated_data.pop('participant_ids', None)
        
        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update participants if provided
        if participant_ids is not None:
            participants = User.objects.filter(user_id__in=participant_ids)
            instance.participants.set(participants)
        
        return instance


class ConversationListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing conversations."""
    participants = UserSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'message_count', 'last_message', 'created_at']
        read_only_fields = ['conversation_id', 'created_at']
    
    def get_message_count(self, obj):
        """Get the count of messages in the conversation."""
        return obj.messages.count()
    
    def get_last_message(self, obj):
        """Get the last message in the conversation."""
        last_message = obj.messages.last()
        if last_message:
            return {
                'message_id': last_message.message_id,
                'sender': UserSerializer(last_message.sender).data,
                'message_body': last_message.message_body,
                'sent_at': last_message.sent_at
            }
        return None

