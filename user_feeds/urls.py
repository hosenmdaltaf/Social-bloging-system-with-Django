from django.urls import path
from .import views
from .views import(
    UserFeedpageListView,
    # PostDetailView,
    PostCreateView, 
    PostUpdateView,
    PostDeleteView 
)  

app_name='user_feeds'

urlpatterns = [
    path('', UserFeedpageListView.as_view(), name='profile-page'),
    path('post/<int:id>',views.postdetail,name='articale-detail'),
    path('post/new',PostCreateView.as_view(),name='post-create'), 
    path('post/<int:pk>/update/', PostUpdateView.as_view(),name='post-update'),
    path('post/<int:pk>/delete/',PostDeleteView.as_view(),name='post-delete'),
]

# path('post/<int:pk>',PostDetailView.as_view(),name='articale-detail'),