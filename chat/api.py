from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import SessionAuthentication
from mychat.settings import MESSAGE_TO_LOAD
from chat.models import MessageModel
from chat.serializers import MessageModelSerializer, UserModelSerializer


# TODO is necessary to delete this class in prod and send CSRF token via POST request
class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    Disabling CSRF tokens fo the API
    """
    def enforce_csrf(self, request):
        return


class MessagePagination(PageNumberPagination):
    """
    Count of messages to be load
    Could be changed in settings.py
    """
    page_size = MESSAGE_TO_LOAD


class MessageModelViewSet(ModelViewSet):
    """
    ModelViewSet for messages
    Provides with .list() and .retrieve() functions
    """
    queryset = MessageModel.objects.all()
    serializer_class = MessageModelSerializer
    allowed_methods = ('GET', 'POST', 'HEAD', 'OPTIONS')
    authentication_classes = (CsrfExemptSessionAuthentication,)  # TODO should be deleted in prod?
    pagination_class = MessagePagination

    def list(self, request, *args, **kwargs):
        """
        Modifies queryset so that only that messages remain
        which related to request.user and request recipient
        """
        self.queryset = self.queryset.filter(Q(recipient=request.user) | Q(user=request.user))
        target = self.request.query_params.get('target', None)
        if target is not None:
            self.queryset = self.queryset.filter(Q(recipient=request.user, user__username=target) |
                                                 Q(recipient__username=target, user=request.user))
        return super(MessageModelViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieving message with request.user and specific id
        """
        message = get_object_or_404(self.queryset.filter(Q(recipient=request.user) |
                                                         Q(user=request.user),
                                                         Q(pk=kwargs['pk'])))
        serializer = self.get_serializer(message)
        return Response(serializer.data)


class UserModelViewSet(ModelViewSet):
    """
    ModelViewSet for users
    Provides with .list() function
    """
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    allowed_methods = ('GET', 'POST', 'OPTIONS')
    pagination_class = None

    def list(self, request, *args, **kwargs):
        """
        Retrieving all users excluding request.user
        TODO should be changed to user.friends or something else
        """
        self.queryset = self.queryset.exclude(id=request.user.id)
        return super(UserModelViewSet, self).list(request, *args, **kwargs)
