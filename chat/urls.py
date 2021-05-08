from django.urls import path
from .import views
from .views import(

      UserListView,
      # chatbox_manager,
    
)

app_name='chat'

urlpatterns =[
    path('inbox/', UserListView.as_view(), name='chat'),
    # path('message/', chatbox_manager, name='extra'),
]
