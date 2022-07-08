from django.urls import path 

from django.contrib.auth.views import LogoutView

from . views import CustomLoginView, RegisterView, ProfileView, FollowSubmitView
# FollowView, , ProfileView

import os
from django.conf import settings

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),

    path('<str:user>/', ProfileView.as_view(), name='profile'),

    path('<int:following_id>/follow', FollowSubmitView.as_view(), name='follow')

   
]