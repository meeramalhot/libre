from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views, logout    ## NEW


urlpatterns = [
  	  path('', VotersListView.as_view(), name="home"),
]