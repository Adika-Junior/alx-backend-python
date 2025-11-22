import logging
import os
from datetime import datetime, time
from collections import defaultdict
from django.http import HttpResponseForbidden, JsonResponse
from django.utils import timezone
from django.conf import settings

# Configure logger for request logging
logger = logging.getLogger('request_logger')
logger.setLevel(logging.INFO)

# Get the project root directory (where manage.py is located)
# __file__ is chats/middleware.py, so we go up two levels to get to project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
log_file_path = os.path.join(BASE_DIR, 'requests.log')

# Create file handler if it doesn't exist
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)

# Add handler to logger if not already added
if not logger.handlers:
    logger.addHandler(file_handler)


class RequestLoggingMiddleware:
    """
    Middleware that logs each user's requests to a file.
    Logs timestamp, user, and request path.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Get user information
        user = request.user if hasattr(request, 'user') and request.user.is_authenticated else 'Anonymous'
        
        # Log the request
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)
        
        # Process the request
        response = self.get_response(request)
        
        return response


class RestrictAccessByTimeMiddleware:
    """
    Middleware that restricts access to the messaging app during certain hours.
    Denies access if user accesses the chat outside 9PM and 6PM.
    Note: This means access is only allowed between 6PM (18:00) and 9PM (21:00).
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Get current server time
        current_time = timezone.now().time()
        
        # Define allowed time range: 6PM (18:00) to 9PM (21:00)
        start_time = time(18, 0)  # 6PM
        end_time = time(21, 0)     # 9PM
        
        # Check if current time is outside the allowed range
        if not (start_time <= current_time <= end_time):
            # Check if the request is for chat-related endpoints
            if 'chat' in request.path.lower() or 'message' in request.path.lower() or 'conversation' in request.path.lower():
                return HttpResponseForbidden(
                    "Access denied. Chat is only available between 6PM and 9PM.",
                    content_type='text/plain'
                )
        
        # Process the request
        response = self.get_response(request)
        
        return response


class OffensiveLanguageMiddleware:
    """
    Middleware that limits the number of chat messages a user can send
    within a certain time window, based on their IP address.
    Implements rate limiting: 5 messages per minute per IP address.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Dictionary to track requests: {ip: [(timestamp1, timestamp2, ...)]}
        self.request_timestamps = defaultdict(list)
        self.max_requests = 5  # Maximum 5 messages
        self.time_window = 60   # Time window in seconds (1 minute)
    
    def __call__(self, request):
        # Only apply rate limiting to POST requests (messages)
        if request.method == 'POST':
            # Check if this is a message-related endpoint
            if 'message' in request.path.lower() or 'chat' in request.path.lower():
                # Get client IP address
                ip_address = self.get_client_ip(request)
                
                # Get current timestamp
                current_time = timezone.now().timestamp()
                
                # Clean old timestamps outside the time window
                self.request_timestamps[ip_address] = [
                    ts for ts in self.request_timestamps[ip_address]
                    if current_time - ts < self.time_window
                ]
                
                # Check if IP has exceeded the limit
                if len(self.request_timestamps[ip_address]) >= self.max_requests:
                    return JsonResponse(
                        {
                            'error': 'Rate limit exceeded',
                            'message': 'You have exceeded the maximum number of messages (5) per minute. Please try again later.'
                        },
                        status=429  # Too Many Requests
                    )
                
                # Add current request timestamp
                self.request_timestamps[ip_address].append(current_time)
        
        # Process the request
        response = self.get_response(request)
        
        return response
    
    def get_client_ip(self, request):
        """Extract client IP address from request."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class RolepermissionMiddleware:
    """
    Middleware that checks the user's role before allowing access to specific actions.
    If the user is not admin or moderator, it returns error 403.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Check if user is authenticated
        if hasattr(request, 'user') and request.user.is_authenticated:
            # Check if this is a chat/message related endpoint that requires admin/moderator
            if 'message' in request.path.lower() or 'chat' in request.path.lower() or 'conversation' in request.path.lower():
                # Get user role
                user_role = getattr(request.user, 'role', None)
                
                # Check if user has admin or moderator role
                # Note: Based on the User model, roles are 'guest', 'host', 'admin'
                # Since there's no 'moderator' in the model, we'll check for 'admin'
                # If moderator is needed, it should be added to the User model
                if user_role not in ['admin']:  # Add 'moderator' here if it exists in the model
                    return HttpResponseForbidden(
                        "Access denied. Admin or moderator role required.",
                        content_type='text/plain'
                    )
        
        # Process the request
        response = self.get_response(request)
        
        return response

