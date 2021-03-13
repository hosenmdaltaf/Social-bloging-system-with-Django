from django.urls import path
from .import views
from .views import(
#     My_profileView,
      ProfileCreateView,
      ProfileUpdateView,
      ProfileDeleteView
)

app_name='profiles'

urlpatterns =[
    path('signup/',views.signup,name='signup'),
    path("login/",views.login_view,name='login'),
    path("logout/",views.logout_view,name='logout'),
    path("my_profile/",views.my_profile,name='my_profile'),
    path('create/', ProfileCreateView.as_view(), name='profile_create'),
    path('update/<int:pk>', ProfileUpdateView.as_view(), name='profile_update'),
    path('delete/<int:pk>', ProfileUpdateView.as_view(), name='profile_delete')

    # path('my_profile/', My_profileView.as_view(), name='my_profile')
]
