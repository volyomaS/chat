from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from chat.api import MessageModelViewSet, UserModelViewSet
from django.contrib.auth.decorators import login_required

# REST API routing
router = DefaultRouter()
router.register(r'message', MessageModelViewSet, basename='message-api')
router.register(r'user', UserModelViewSet, basename='user-api')

urlpatterns = [
    path(r'api/v1/', include(router.urls)),
    path('', login_required(views.room), name='home')
]
