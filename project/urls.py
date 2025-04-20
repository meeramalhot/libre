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
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='show_profile'),
    path('profile/book_upload', BookUploadView.as_view(), name="book_upload"),
    path('profile/rev_upload', ReviewUploadView.as_view(), name="review_upload"),

    path('profiles/<int:pk>/analytics/', UserAnalyticsView.as_view(), name='analytics'),


    path('profile/<int:pk>/delete', DeleteReviewView.as_view(), name='delete'),
    path('profile/add_friend/<int:other_pk>/', AddFriendView.as_view(), name='add_friend'),
    path('profile/friend_suggestions/', ShowFriendSuggestionsView.as_view(), name='friend_suggest'),
    path('profile/feed/', ShowFeedView.as_view(), name='feed'),
    path('profile/review/<int:pk>/update/', UpdateReviewView.as_view(), name='update'),


    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'), ## NEW
    path('logout/', auth_views.LogoutView.as_view(template_name='project/logout.html'), name='logout'),
    path('create_profile/', CreateProfileView.as_view(), name="make_profile"),


]