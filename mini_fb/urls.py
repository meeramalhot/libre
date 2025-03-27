'''
author: meera malhotra
date: 2/20
filename: urls.py
description: url paths for mini_fb
'''

from django.urls import path
from .views import * #ShowAllProfilesView, ShowProfilePageView, CreateArticleView
from django.contrib.auth import views as auth_views, logout    ## NEW


urlpatterns = [
  path('', ShowAllProfilesView.as_view(), name="show_all_profiles"),
  path('show_all_profiles', ShowAllProfilesView.as_view(), name="show_all_profiles"),
  path('profile/<int:pk>/', ShowProfilePageView.as_view(), name="show_profile"),
  path('create_profile/', CreateArticleView.as_view(), name="create_profile"),
  path('profile/create_status', CreateStatusMessageView.as_view(), name="create_status"),
  path('profile/update', UpdateProfileView.as_view(), name="update_profile"), # NEW
  path('status/<int:pk>/delete', DeleteStatusMessageView.as_view(), name='delete'),  ## NEW
  path('status/<int:pk>/update', UpdateStatusMessageView.as_view(), name='update'),  ## NEW
  path('profile/add_friend/<int:other_pk>/', AddFriendView.as_view(), name='add_friend'),
  path('profile/friend_suggestions/', ShowFriendSuggestionsView.as_view(), name='friend_suggestions'),
  path('profile/news_feed/', ShowNewsFeedView.as_view(), name='news_feed'),
  path('login/', auth_views.LoginView.as_view(template_name='mini_fb/login_here.html'), name='login'), ## NEW
  path('logout/', auth_views.LogoutView.as_view(template_name='mini_fb/logout_here.html'), name='logout'),
  #path('register/', RegistrationView.as_view(), name='register'),

]
