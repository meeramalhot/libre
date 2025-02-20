'''
author: meera malhotra
date: 2/20
filename: urls.py
description: url paths for mini_fb
'''

from django.urls import path
from .views import ShowAllProfilesView, ShowProfilePageView

urlpatterns = [
  path('', ShowAllProfilesView.as_view(), name="show_all_profiles"),
  path('show_all_profiles', ShowAllProfilesView.as_view(), name="show_all_profiles"),
  path('profile/<int:pk>/', ShowProfilePageView.as_view(), name="show_profile"),

]