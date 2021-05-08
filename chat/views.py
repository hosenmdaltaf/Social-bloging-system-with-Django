from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.db.models import Q

# from django_private_chat2.models import MessageModel


# @login_required(login_url ='/profiles/login/')
# def  chatbox_manager(request):
# 	followers = request.user.profile.followers
# 	following = request.user.following
# 	chat_all = MessageModel.objects.all()
# 	existing_chats = MessageModel.objects.filter(Q(sender_id=request.user) | Q(recipient_id=request.user))
# 	existing_chat_index = {}

# 	for chat in existing_chats:
# 		if chat.sender_id == request.user.pk:
# 			existing_chat_index[chat.recipient_id] = chat.pk
# 		else:
# 			existing_chat_index[chat.sender_id] = chat.pk

# 	for user in followers.all():
# 		if user.pk in existing_chat_index.keys():
# 			del existing_chat_index[user.pk]
# 		else:
# 			MessageModel.objects.create(sender_id=request.user.pk, recipient_id=user.pk, text=settings.DEFAULT_GRETING_TEXT_IN_CHAT)

# 	for value in existing_chat_index.values():
# 		MessageModel.objects.filter(pk=value).delete()

# 	print(MessageModel.objects.all().count())

# 	print('#'*10)
# 	print(len(existing_chat_index))
# 	print(existing_chats.count())
# 	print(chat_all.count())
# 	print('#'*10)

# 	return redirect('chat:inbox')


@method_decorator(login_required, name='dispatch')
class UserListView(ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = 'chat/chats.html'
    login_url = '/profiles/login/'