from django.urls import path
from homepage.views import HomepageListView

app_name='homepage'

urlpatterns = [
    path('', HomepageListView.as_view(), name='article-list'),
]
