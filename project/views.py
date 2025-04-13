from typing import Any
from django.shortcuts import render, redirect
from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View, TemplateView
#from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm, UpdateStatusForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin ## NEW
from django.contrib.auth.forms import UserCreationForm ## NEW
from django.contrib.auth.models import User ## NEW
from django.contrib.auth import login # NEW
from django.contrib.auth.views import LoginView  # NEW


class ShowAllProfilesView(ListView):
    '''Create a subclass of ListView to display all blog profiles.'''

    model = UserProfile # retrieve objects of type Article from the database
    template_name = 'project/show_all.html'
    context_object_name = 'profiles' # how to find the data in the template file

class ProfileDetailView(DetailView):
    model = UserProfile
    template_name = 'project/profile_detail.html'  # create this template as needed.
    context_object_name = 'profile'