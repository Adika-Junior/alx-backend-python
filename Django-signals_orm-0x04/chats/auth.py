"""
Authentication configuration for the messaging app.

This module provides JWT authentication settings and customizations
for user authentication in the messaging application.
"""
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom token serializer that includes user_id in the token payload.
    
    This ensures that the JWT token contains the user_id field
    which is used as the primary key in the User model.
    """
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add user_id to token payload
        token['user_id'] = str(user.user_id)
        return token


class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom JWT Authentication class that validates tokens
    and ensures users can access their own data.
    
    This extends the default JWT authentication to provide
    additional validation and user context.
    """
    
    def get_user(self, validated_token):
        """
        Get the user from the validated token.
        
        Args:
            validated_token: The validated JWT token
            
        Returns:
            User instance from the token
            
        Raises:
            InvalidToken: If user is not found or inactive
        """
        try:
            # Try to get user_id from token (custom claim)
            user_id = validated_token.get('user_id')
            
            # Fallback to 'id' claim if user_id is not present
            if user_id is None:
                user_id = validated_token.get('id') or validated_token.get('user_id')
            
            if user_id is None:
                raise InvalidToken('Token contained no user identifier')
            
            user = User.objects.get(user_id=user_id)
            
            if not user.is_active:
                raise InvalidToken('User is inactive or deleted')
            
            return user
        except User.DoesNotExist:
            raise InvalidToken('User not found')
        except Exception as e:
            raise InvalidToken(f'Error getting user: {str(e)}')

