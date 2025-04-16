from typing import Any
from django.shortcuts import render, redirect
from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View, TemplateView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin ## NEW
from django.contrib.auth.forms import UserCreationForm ## NEW
from django.contrib.auth.models import User ## NEW
from django.contrib.auth import login # NEW
from django.contrib.auth.views import LoginView  # NEW
from .forms import *
from django.utils import timezone



class ShowAllProfilesView(ListView):
    '''Create a subclass of ListView to display all blog profiles.'''

    model = UserProfile # retrieve objects of type Article from the database
    template_name = 'project/show_all.html'
    context_object_name = 'profiles' # how to find the data in the template file


    def dispatch(self, request, *args, **kwargs):
        '''Override the dispatch method to add debugging information.'''

        if request.user.is_authenticated:
            print(f'ShowAllView.dispatch(): request.user={request.user}')
        else:
            print(f'ShowAllView.dispatch(): not logged in.')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=self.request.user)
            except UserProfile.DoesNotExist:
                profile = None
            
            context['profile'] = profile
        return context


class ProfileDetailView(DetailView):
    model = UserProfile
    template_name = 'project/prof_detail.html'
    context_object_name = 'profiles'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:

            profile = UserProfile.objects.get(user=self.request.user)
            context['profile'] = profile

        return context

class CreateProfileView(CreateView):
    '''A view to handle creation of a new profile.
    (1) display the HTML form to user (GET)
    (2) process the form submission and store the new Article object (POST)
    '''

    form_class = MakeProfileForm
    template_name = 'project/make_profile.html'
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        # add to context
        context['user_creation_form'] = UserCreationForm()
        return context
    
    def form_valid(self, form):
        user_form = UserCreationForm(self.request.POST)
        if user_form.is_valid():
                new_user = user_form.save()
                login(self.request, new_user)
                form.instance.user = new_user
                form.instance.date_joined = timezone.now()
                
                return super().form_valid(form)
        else:
                    print("invalid form!")
                    return self.form_invalid(form)
        
    def get_login_url(self) -> str:
        return reverse('login')


#https://stackoverflow.com/questions/1395807/proper-way-to-handle-multiple-forms-on-one-page-in-django
class CreateReviewView(LoginRequiredMixin, CreateView):
        '''A view to handle creation of a new Comment on an Article.'''

        template_name = "project/create_status_form.html"

        def get_success_url(self):
            '''Provide a URL to redirect to after creating a new status message.'''
            profile = UserProfile.objects.get(user=self.request.user)
            return reverse('show_profile', kwargs={'pk': profile.pk})
        
        def get_context_data(self, **kwargs):
            '''Return the dictionary of context variables for use in the template.'''
            context = super().get_context_data(**kwargs)

            profile = UserProfile.objects.get(user=self.request.user)
            context['profile'] = profile
            return context
        
        def get_login_url(self) -> str:
            '''return the URL required for login'''
            return reverse('login')
        
        def get_object(self):
            return UserProfile.objects.get(user=self.request.user)