from django.urls import path
from .import views
# from homepage.views import HomepageListView

app_name='homepage'

urlpatterns = [
    path('',views.home,name='article-list'),
    # path('latest/',views.latest,name='latest-list')
    # path('', HomepageListView.as_view(), name='article-list'),
    # path('post/<int:id>',views.postdetail,name='articale-detail'),
]
