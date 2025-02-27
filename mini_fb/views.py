'''
author: meera malhotra
date: 2/20
filename: views.py
description: displaying different amounts of profiles for html
'''

from django.shortcuts import render
from .models import Profile, StatusMessage
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse

class ShowAllProfilesView(ListView):
    '''Create a subclass of ListView to display all blog profiles.'''

    model = Profile # retrieve objects of type Article from the database
    template_name = 'mini_fb/show_all.html'
    context_object_name = 'profiles' # how to find the data in the template file


class ShowProfilePageView(DetailView):
    """
    Show the details for one profile
    """
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profiles'