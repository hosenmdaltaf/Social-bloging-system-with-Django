from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import SessionAuthentication

from altaf import settings
from core.serializers import MessageModelSerializer, UserModelSerializer,GroupMessageSerializer,GroupSerializer
from core.models import MessageModel,GroupMessage,Group


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    SessionAuthentication scheme used by DRF. DRF's SessionAuthentication uses
    Django's session framework for authentication which requires CSRF to be
    checked. In this case we are going to disable CSRF tokens for the API.
    """

    def enforce_csrf(self, request):
        return


class MessagePagination(PageNumberPagination):
    """
    Limit message prefetch to one page.
    """
    page_size = settings.MESSAGES_TO_LOAD


class MessageModelViewSet(ModelViewSet):
    queryset = MessageModel.objects.all()
    serializer_class = MessageModelSerializer
    allowed_methods = ('GET', 'POST', 'HEAD', 'OPTIONS')
    authentication_classes = (CsrfExemptSessionAuthentication,)
    pagination_class = MessagePagination

    def list(self, request, *args, **kwargs):
        target = self.request.query_params.get('target', None)
        if target is not None:
            self.queryset = self.queryset.filter(
                Q(recipient=request.user, user__username=target) |
                Q(recipient__username=target, user=request.user))
            return super(MessageModelViewSet, self).list(request, *args, **kwargs)
        else:
            print("handle get without parameters")
            
    # @ POST
    # @ /api/v1/message/ 
    # @ Description: receives message to be sent, saves it and notifies users
    def create(self, request, *args, **kwargs):
        self.serializer_class(data=request.data)
        return super(MessageModelViewSet, self).create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        msg = get_object_or_404(
            self.queryset.filter(Q(recipient=request.user) |
                                 Q(user=request.user),
                                 Q(pk=kwargs['pk'])))
        serializer = self.get_serializer(msg)
        return Response(serializer.data)


class UserModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    allowed_methods = ('GET', 'HEAD', 'OPTIONS')
    pagination_class = None  # Get all user

    def list(self, request, *args, **kwargs):
        # Get all users except yourself
        self.queryset = self.queryset.exclude(id=request.user.id)
        return super(UserModelViewSet, self).list(request, *args, **kwargs)
class GroupMessageViewSet(ModelViewSet):
    queryset = GroupMessage.objects.all()
    serializer_class = GroupMessageSerializer
    allowed_methods = ('GET', 'POST', 'HEAD', 'OPTIONS')
    authentication_classes = (CsrfExemptSessionAuthentication,)
    pagination_class = MessagePagination

    # # Change this soon
    def list(self, request, *args, **kwargs):
        target = self.request.query_params.get('target', None)
        if target is not None:
            self.queryset = self.queryset.filter(group__name=target)
        return super(GroupMessageViewSet, self).list(request, *args, **kwargs)
    # @ POST
    # @ /api/v1/message/ 
    # @ Description: receives message to be sent, saves it and notifies users
    def create(self, request, *args, **kwargs):
        group = request.data['group']
        body = request.data['body']
        sender = request.user
        group = get_object_or_404(
            Group, name=group)
        msg = GroupMessage(sender=sender,
                           body=body,
                           group=group)
        msg.save()
        return Response({"message":"succes"})
    
    def retrieve(self, request, *args, **kwargs):
        msg = get_object_or_404(
            self.queryset.filter(Q(pk=kwargs['pk'])))
        serializer = self.get_serializer(msg)
        return Response(serializer.data)

class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    allowed_methods = ('GET', 'HEAD', 'OPTIONS')
    pagination_class = None  # Get all user

    def list(self, request, *args, **kwargs):
        target = self.request.query_params.get('target', None)
        print(target)
        if target is not None:
            groups = Group.objects.all()
            user = User.objects.get(username=target)
            self.queryset = [x for x in groups if x.has(user.id)]
        return super(GroupViewSet, self).list(request, *args, **kwargs)
