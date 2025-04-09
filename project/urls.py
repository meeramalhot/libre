'''
author: meera malhotra
date: 4/9
filename: urls.py
description: url paths for final project
'''

from django.urls import path
from .views import * #ShowAllProfilesView, ShowProfilePageView, CreateArticleView
from django.contrib.auth import views as auth_views, logout    ## NEW


urlpatterns = [ ]