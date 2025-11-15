from django.urls import path, include
from rest_framework import routers
from drf_nested_routers import NestedDefaultRouter
from .views import ConversationViewSet, MessageViewSet

# Create a router and register our viewsets
# Using routers.DefaultRouter() to automatically create endpoints
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Create nested router for messages within conversations
nested_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
nested_router.register(r'messages', MessageViewSet, basename='conversation-messages')

# Also register messages at the top level for direct access
router.register(r'messages', MessageViewSet, basename='message')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
    path('', include(nested_router.urls)),
]

