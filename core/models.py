from django.contrib.auth.models import User
from django.db.models import (Model, TextField, DateTimeField, ForeignKey,
                              CASCADE)

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import models
import json


class MessageModel(Model):
    """
    This class represents a chat message. It has a owner (user), timestamp and
    the message body.

    """
    user = ForeignKey(User, on_delete=CASCADE, verbose_name='user',
                      related_name='from_user', db_index=True)
    recipient = ForeignKey(User, on_delete=CASCADE, verbose_name='recipient',
                           related_name='to_user', db_index=True)
    timestamp = DateTimeField('timestamp', auto_now_add=True, editable=False,
                              db_index=True)
    body = TextField('body')

    def __str__(self):
        return str(self.id)

    def characters(self):
        """
        Toy function to count body characters.
        :return: body's char number
        """
        return len(self.body)

    def notify_ws_clients(self):
        """
        Inform client there is a new message.
        """
        notification = {
            'type': 'chat_message',
            'message': '{}'.format(self.id)
        }

        channel_layer = get_channel_layer()
        print("user.id {}".format(self.user.id))
        print("user.id {}".format(self.recipient.id))

        async_to_sync(channel_layer.group_send)("{}".format(self.user.id), notification)
        async_to_sync(channel_layer.group_send)("{}".format(self.recipient.id), notification)

    def save(self, *args, **kwargs):
        """
        Trims white spaces, saves the message and notifies the recipient via WS
        if the message is new.
        """
        new = self.id
        self.body = self.body.strip()  # Trimming whitespaces from the body
        super(MessageModel, self).save(*args, **kwargs)
        if new is None:
            self.notify_ws_clients()

    # Meta
    class Meta:
        app_label = 'core'
        verbose_name = 'message'
        verbose_name_plural = 'messages'
        ordering = ('-timestamp',)

class Group(models.Model):
    name = models.CharField(max_length = 20)
    members = models.TextField()
    messages = models.TextField ()
    
    def set_members(self,user_id_list):
        self.members = json.dumps(user_id_list)
    def get_members(self):
        return json.loads(self.members)
    def add(self,user_id):
        current_list = self.get_members()
        if user_id in current_list:
            print("user is already in the group")
        else:
            new_list = current_list.append(user_id)
            self.set_members(new_list)
    def remove(self,user_id):
        current_list = self.get_members()
        if user_id in current_list:
            new_list = current_list.remove(user_id)
            self.set_members(new_list)
        else:
            print("User is not a member of theis group")
            
    def has(self,user_id):
        current_list = self.get_members()
        return(user_id in current_list)
    
    # Set of functions for dealing with group messages

    def set_messages(self,message_id_list):
        self.messages = json.dumps(message_id_list)
    def get_messages(self):
        return json.loads(self.messages)
    def add_message(self,message_id):
        current_list = self.get_messages()
        new_list = current_list.append(message_id)
        self.set_messages(new_list)
        
    def delete_message(self,message_id):
        current_list = self.get_messages()
        if message_id in current_list:
            new_list = current_list.remove(message_id)
            self.set_messages(new_list)


    def save(self, *args, **kwargs): 
        if self.pk is None or self.members is None or self.members == '':
            self.set_members([])
        if self.pk is None or self.messages is None or self.messages == '':
            self.set_messages([])
        super(Group, self).save(*args, **kwargs)
    def __str__(self):
        return self.name+" ID: "+str(self.id)
    # Meta
    class Meta:
        app_label = 'core'
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'
        ordering = ('name',)

class GroupMessage(Model):
    """
    This class represents a chat message. It has a owner (user), timestamp and
    the message body.

    """
    sender = ForeignKey(User, on_delete=CASCADE, verbose_name='sender',
                      related_name='from_sender', db_index=True)
    group = ForeignKey(Group, on_delete=CASCADE, verbose_name='group',
                           related_name='to_group', db_index=True)
    time = DateTimeField('time', auto_now_add=True, editable=False,
                              db_index=True)
    body = TextField('body')

    def __str__(self):
        return str(self.id)

    def characters(self):
        """
        Toy function to count body characters.
        :return: body's char number
        """
        return len(self.body)

    def notify_ws_clients(self):
        """
        Inform client there is a new message.
        """
        notification = {
            'type': 'group_message',
            'group': '{}'.format(self.id)
        }

        channel_layer = get_channel_layer()
        group_id = "group"+str(self.group.id)
        print("group.id {}".format(group_id))
        async_to_sync(channel_layer.group_send)(group_id, notification)

    def save(self, *args, **kwargs):
        """
        Trims white spaces, saves the message and notifies the recipient via WS
        if the message is new.
        """
        new = self.id
        self.body = self.body.strip()  # Trimming whitespaces from the body
        super(GroupMessage, self).save(*args, **kwargs)
        if new is None:
            self.notify_ws_clients()

    # Meta
    class Meta:
        app_label = 'core'
        verbose_name = 'group message'
        verbose_name_plural = 'group messags'
        ordering = ('-time',)
