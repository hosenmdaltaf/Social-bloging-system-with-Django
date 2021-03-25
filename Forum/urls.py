from django.urls import path
from .import views
from .views import(
   DiscussCreateView,
   DiscussUpdateView,
   DiscussDeleteView,
  #  DiscussDetailView 
 ) 
app_name='Forum'

urlpatterns = [
    path('',views.discuss_seaction_home,name='forum_homepage'),
    path('create/', DiscussCreateView.as_view(), name='profile_create'),
    path('update/<int:pk>', DiscussUpdateView.as_view(), name='profile_update'),
    path('delete/<int:pk>', DiscussDeleteView.as_view(), name='profile_delete'),
    # path('discuss/<int:pk>',DiscussDetailView.as_view(),name='articale-detail')
    path('discuss/<int:id>',views.discuss_seaction_details,name='articale-detail')
   
]


