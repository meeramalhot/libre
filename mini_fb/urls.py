from django.urls import path
from mini_fb.views import ShowAllProfilesView

urlpatterns = [
  path('show_all', ShowAllProfilesView.as_view(), name="show_all"),
]