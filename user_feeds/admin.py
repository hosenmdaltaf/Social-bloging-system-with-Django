from django.contrib import admin
from user_feeds.models import Post,Comment,Category


admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Post)

# class AuthorAdmin(admin.ModelAdmin):
#     list_display  = ('author', 'title', 'post_date','category')
#     list_filter = ('author', 'title',)
#     # search_fields = ['writer',]

# admin.site.register(Post, AuthorAdmin)
