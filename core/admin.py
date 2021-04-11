from django.contrib.admin import ModelAdmin, site
from core.models import MessageModel
from core.models import MessageModel, Group,GroupMessage


class MessageModelAdmin(ModelAdmin):
    readonly_fields = ('timestamp',)
    search_fields = ('id', 'body', 'user__username', 'recipient__username')
    list_display = ('id', 'user', 'recipient', 'timestamp', 'characters')
    list_display_links = ('id',)
    list_filter = ('user', 'recipient')
    date_hierarchy = 'timestamp'
class GroupAdmin(ModelAdmin):
    readonly_fields = ('members','messages',)
    search_fields = ('id', 'name',)
    list_display = ('id', 'name',)
    list_display_links = ('id','name',)
    list_filter = ('name',)
class GroupMessageAdmin(ModelAdmin):
    readonly_fields = ('time',)
    search_fields = ('id', 'body', 'sender__username', 'sender__name')
    list_display = ('id', 'sender', 'group', 'time', 'characters')
    list_display_links = ('id',)
    list_filter = ('sender', 'group')
    date_hierarchy = 'time'


site.register(MessageModel, MessageModelAdmin)
site.register(Group, GroupAdmin)
site.register(GroupMessage, GroupMessageAdmin)