from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from rest_framework.routers import DefaultRouter
from core.api import MessageModelViewSet, UserModelViewSet,GroupMessageViewSet,GroupViewSet



router = DefaultRouter()
router.register(r'message', MessageModelViewSet, basename='message-api')
router.register(r'user', UserModelViewSet, basename='user-api')
#Groups
router.register(r'group/message', GroupMessageViewSet, basename='group-message-api')
router.register(r'group', GroupViewSet, basename='group-api')

app_name ='core'

urlpatterns = [
    path(r'api/v1/', include(router.urls)),

    path('', login_required(
        TemplateView.as_view(template_name='core/chat.html')), name='home'),
]
