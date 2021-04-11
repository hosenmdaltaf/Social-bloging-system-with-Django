
# chat/consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Group,MessageModel,GroupMessage
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user_id = self.scope["session"]["_auth_user_id"]
        self.group_name = "{}".format(user_id)
        # Join room group

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data=None,bytes_data = None):

        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # Send message to room group
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'recieve_group_message',
                'message': message
            }
        )

    async def recieve_group_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(
             text_data=json.dumps({
            'message': message
        }))

class SyncChatConsumer(WebsocketConsumer):
    def connect(self):
        user_id = self.scope["session"]["_auth_user_id"]
        self.group_name = "{}".format(user_id)

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        groups = Group.objects.all()
        for group in groups:
            if group.has(int(self.group_name)):
                group_id = "group"+str(group.id)
                async_to_sync(self.channel_layer.group_add)(
                    group_id,
                    self.channel_name
                )


        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json['message']
        sender = text_data_json['sender']
        key = text_data_json['group']

        # creat a new message and save
        group = get_object_or_404(
            Group, id=int(key))
        sender = get_object_or_404(
            User, username = str(sender))
        msg = GroupMessage(sender=sender,
                           body=body,
                           group=group)
        msg.save()
         

        group_id = "group"+str(key)
        # Send message to room group
        # async_to_sync(self.channel_layer.group_send)(
        #     group_id,
        #     {
        #         'type': 'chat_message',
        #         'message': msg.id
        #     }
        # )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'group':False
        }))
    # Receive message from groups
    def group_message(self, event):
        group = event['group']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': group,
            'group':True
        }))