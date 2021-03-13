from django.shortcuts import render
from django.views.generic.list import ListView
from user_feeds.models import Post


class HomepageListView(ListView):
    model = Post
    # paginate_by = 10
    template_name='homepage/homepage.html'
