'''
author: meera malhotra
date: 2/20
filename: urls.py
description: url paths for mini_fb
'''

from django.urls import path
from .views import * #ShowAllProfilesView, ShowProfilePageView, CreateArticleView

urlpatterns = [
  path('', ShowAllProfilesView.as_view(), name="show_all_profiles"),
  path('show_all_profiles', ShowAllProfilesView.as_view(), name="show_all_profiles"),
  path('profile/<int:pk>/', ShowProfilePageView.as_view(), name="show_profile"),
  path('create_profile/', CreateArticleView.as_view(), name="create_profile"),
  path('profile/<int:pk>/create_status', CreateStatusMessageView.as_view(), name="create_status"),
  path('profile/<int:pk>/update', UpdateProfileView.as_view(), name="update_profile"), # NEW
  path('status/<int:pk>/delete', DeleteStatusMessageView.as_view(), name='delete'),  ## NEW
  path('status/<int:pk>/update', UpdateStatusMessageView.as_view(), name='update'),  ## NEW
  path('profile/<int:pk>/add_friend/<int:other_pk>/', AddFriendView.as_view(), name='add_friend'),
  path('profile/<int:pk>/friend_suggestions/', ShowFriendSuggestionsView.as_view(), name='friend_suggestions'),
  path('profile/<int:pk>/news_feed/', ShowNewsFeedView.as_view(), name='news_feed'),

]