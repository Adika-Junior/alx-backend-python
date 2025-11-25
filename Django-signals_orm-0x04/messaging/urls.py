from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MessageViewSet, delete_user

router = DefaultRouter()
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
    path('delete-user/', delete_user, name='delete-user'),
]

