from django.urls import path
from .import views
from .views import(
#     My_profileView,
      ProfileCreateView,
      ProfileUpdateView,
      ProfileDeleteView,
      Profile_list_View,
      ProfileDetailView,
      SearchResultsView
    #   My_ProfileDetailView
)

app_name='profiles'

urlpatterns =[
    path('signup/',views.signup,name='signup'),
    path("login/",views.login_view,name='login'),
    path("logout/",views.logout_view,name='logout'),
    path("logout/",views.logout_view,name='logout'),
    path("swith_follow/",views.follow_and_unfolow,name='follow_and_unfolow'),

    # path("<int:id>/",views.profiles_detail,name='my_profile'),
    path('<int:pk>/',ProfileDetailView.as_view(), name='my_profile'),
    path('all_profile/', Profile_list_View.as_view(), name='all_profile'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('create/', ProfileCreateView.as_view(), name='profile_create'),
    path('update/<int:pk>', ProfileUpdateView.as_view(), name='profile_update'),
    path('delete/<int:pk>', ProfileUpdateView.as_view(), name='profile_delete'),

    # path('my_profile/', My_profileView.as_view(), name='my_profile')
]

