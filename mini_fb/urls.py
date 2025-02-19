from django.urls import path
from mini_fb.views import ShowAllProfilesView, ShowProfilePageView

urlpatterns = [
  path('', ShowAllProfilesView.as_view(), name="show_all_profiles"),
  path('show_all_profiles', ShowAllProfilesView.as_view(), name="show_all_profiles"),
  path('profile/<int:pk>/', ShowProfilePageView.as_view(), name="show_profile"),

]