'''
author: meera malhotra
date: 4/9
filename: urls.py
description: url paths for final project
'''

from django.urls import path
from .views import * #ShowAllProfilesView, ShowProfilePageView, CreateArticleView
from django.contrib.auth import views as auth_views, logout    ## NEW


urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name="profiles_all"),
    path('profiles/', ShowAllProfilesView.as_view(), name='profiles_all'),
    path('profiles/<int:pk>/', ProfileDetailView.as_view(), name='show_profile'),
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'), ## NEW
    path('logout/', auth_views.LogoutView.as_view(template_name='project/logout.html'), name='logout'),
    path('create_profile/', CreateProfileView.as_view(), name="make_profile"),


]