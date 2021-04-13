from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from core.models import MessageModel,GroupMessage,Group
from rest_framework.serializers import ModelSerializer, CharField


class MessageModelSerializer(ModelSerializer):
    user = CharField(source='user.username', read_only=True)
    recipient = CharField(source='recipient.username')

    def create(self, validated_data):
        user = self.context['request'].user
        recipient = get_object_or_404(
            User, username=validated_data['recipient']['username'])
        msg = MessageModel(recipient=recipient,
                           body=validated_data['body'],
                           user=user)
        msg.save()
        return msg

    class Meta:
        model = MessageModel
        fields = ('id', 'user', 'recipient', 'timestamp', 'body')
class GroupMessageSerializer(ModelSerializer):
    sender = CharField(source='sender.username', read_only=True)
    group = CharField(source='group.name', read_only=True)
    class Meta:
        model = GroupMessage
        fields = '__all__'


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)
class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'