from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views, logout    ## NEW


urlpatterns = [
  	  path('', VotersListView.as_view(), name="home"),
      path('voter/<int:pk>', VoterDetailView.as_view(), name="voter"),
      path('graphs', VoterGraphView.as_view(), name="graphs")
]
