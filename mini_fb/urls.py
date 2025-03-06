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
]