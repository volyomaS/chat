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


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class MessagePagination(PageNumberPagination):
    page_size = MESSAGE_TO_LOAD


class MessageModelViewSet(ModelViewSet):
    queryset = MessageModel.objects.all()
    serializer_class = MessageModelSerializer
    allowed_methods = ('GET', 'POST', 'HEAD', 'OPTIONS')
    authentication_classes = (CsrfExemptSessionAuthentication,)
    pagination_class = MessagePagination

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(Q(recipient=request.user) | Q(user=request.user))
        target = self.request.query_params.get('target', None)
        if target is not None:
            self.queryset = self.queryset.filter(Q(recipient=request.user, user__username=target) |
                                                 Q(recipient__username=target, user=request.user))
        return super(MessageModelViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        message = get_object_or_404(self.queryset.filter(Q(recipient=request.user) |
                                                         Q(user=request.user),
                                                         Q(pk=kwargs['pk'])))
        serializer = self.get_serializer(message)
        return Response(serializer.data)


class UserModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    allowed_methods = ('GET', 'POST', 'OPTIONS')
    pagination_class = None

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.exclude(id=request.user.id)
        return super(UserModelViewSet, self).list(request, *args, **kwargs)
