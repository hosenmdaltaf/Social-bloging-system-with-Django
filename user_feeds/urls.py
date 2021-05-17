from django.urls import path
from .import views
from .views import(
    # UserFeedpageListView,
    # PostDetailView,
    PostCreateView, 
    PostUpdateView,
    PostDeleteView 
)  

app_name='user_feeds'

urlpatterns = [
    path('',views.userFeedpage,name='profile-page'),
    path('post/<int:id>',views.postdetail,name='articale-detail'),
    path('post/new',PostCreateView.as_view(),name='post-create'), 
    path('post/<int:pk>/update/', PostUpdateView.as_view(),name='post-update'),
    path('post/<int:pk>/delete/',PostDeleteView.as_view(),name='post-delete'),

    path('fav/<int:id>/', views.favourite_add, name='favourite_add'),
    path('profile/favourites/', views.favourite_list, name='favourite_list'),
 
]
