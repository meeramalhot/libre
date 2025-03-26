'''
author: meera malhotra
date: 2/20
filename: views.py
description: displaying different amounts of profiles for html
'''

from django.shortcuts import render, redirect
from .models import Profile, StatusMessage, Image, StatusImage, Friend
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from .forms import CreateProfileForm, CreateStatusMessageForm, UpdateProfileForm, UpdateStatusForm
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin ## NEW


class ShowAllProfilesView(ListView):
    '''Create a subclass of ListView to display all blog profiles.'''

    model = Profile # retrieve objects of type Article from the database
    template_name = 'mini_fb/show_all.html'
    context_object_name = 'profiles' # how to find the data in the template file

    def dispatch(self, request, *args, **kwargs):
        '''Override the dispatch method to add debugging information.'''

        if request.user.is_authenticated:
            print(f'ShowAllView.dispatch(): request.user={request.user}')
        else:
            print(f'ShowAllView.dispatch(): not logged in.')

        return super().dispatch(request, *args, **kwargs)


class ShowProfilePageView(DetailView):
    """
    Show the details for one profile
    """
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profiles'


class CreateArticleView(LoginRequiredMixin, CreateView):
    '''A view to handle creation of a new profile.
    (1) display the HTML form to user (GET)
    (2) process the form submission and store the new Article object (POST)
    '''

    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')


class CreateStatusMessageView(LoginRequiredMixin, CreateView):
    '''A view to handle creation of a new Comment on an Article.'''

    form_class = CreateStatusMessageForm
    template_name = "mini_fb/create_status_form.html"

    def get_success_url(self):
        '''Provide a URL to redirect to after creating a new Comment.'''
        # return reverse('show_all')
        #retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        #call reverse to generate the URL for this Article
        return reverse('show_profile', kwargs={'pk':pk})
    
    def get_context_data(self):
        '''Return the dictionary of context variables for use in the template'''

        #calling the superclass method
        context = super().get_context_data()

        # find/add the profile to the context data
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)

        # add this profile into the context dictionary:
        context ['profile'] = profile
        return context 
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    

    def form_valid(self, form):
        '''This method handles the form submission and saves the new object to the Django database.
        We need to add the foreign key (of the Article) to the Comment object before saving it to the database
        '''

        print(form.cleaned_data)
        #retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        # attach this article to the comment
        form.instance.profile = profile # set the FK

        # save the status message to database
        sm = form.save()

        # read the file from the form:
        files = self.request.FILES.getlist('files')

        for file in files:
            #Create an Image object, and set the file into the Image‘s ImageField attribute
            #call the Image‘s .save() method to save the Image object to the database
            new_image = Image(profile=profile, image_file=file)
            new_image.save()

            # Create and save a StatusImage object that sets the foreign keys of the StatusMessage and the Image objects
            #then call the StatusImage object’s .save() method to save the Image object to the database.

            new_status = StatusImage(status_message=sm, image=new_image)
            new_status.save()


        # delegate the work to the superclass method form_valid:
        return super().form_valid(form)

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    '''Allows u to update profile'''
    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_fb/update_profile_form.html"

    def get_success_url(self):
        '''Return the URL to redirect to after updating the profile.'''
        # get the pk for this profile
        pk = self.kwargs.get('pk')
        profile = Profile.objects.get(pk=pk)
        
        # reverse to show the profile detail page
        return reverse('show_profile', kwargs={'pk': profile.pk})
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    

class DeleteStatusMessageView(LoginRequiredMixin, DeleteView):
    '''Allows u to delete a status message'''

    template_name = "mini_fb/delete_status_form.html"
    model = StatusMessage
    context_object_name = 'status_message'

    def get_success_url(self):
        '''Return a the URL to which we should be directed after the delete.'''

        # get the pk for this sm
        pk = self.kwargs.get('pk')
        sm = StatusMessage.objects.get(pk=pk)
        
        # find the Status Message to which this Profile is related by FK
        profile = sm.profile
        
        # reverse to show the article page
        return reverse('show_profile', kwargs={'pk':profile.pk})
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    

class UpdateStatusMessageView(LoginRequiredMixin, UpdateView):
    '''Allows u to update a status message'''

    template_name = "mini_fb/update_status_form.html"
    form_class= UpdateStatusForm
    model = StatusMessage
    context_object_name = 'status_message'

    def get_success_url(self):
        '''Return a the URL to which we should be directed after the update.'''

        # get the pk for this sm
        pk = self.kwargs.get('pk')
        sm = StatusMessage.objects.get(pk=pk)
        
        # find the Status Message to which this Profile is related by FK
        profile = sm.profile
        
        # reverse to show the article page
        return reverse('show_profile', kwargs={'pk':profile.pk})
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    

class AddFriendView(View):
    def dispatch(self, request, *args, **kwargs):
        profile_pk = self.kwargs['pk']
        other_pk = self.kwargs['other_pk']

        friend_one = Profile.objects.get(pk=profile_pk)
        friend_two = Profile.objects.get(pk=other_pk)

        friend_one.add_friend(friend_two)
        
        return redirect('show_profile', pk=friend_one.pk)
    

    
class ShowFriendSuggestionsView(DetailView):
    model = Profile
    template_name = "mini_fb/friend_suggestions.html"
    context_object_name = "profile"

class ShowNewsFeedView(DetailView):
    model = Profile
    template_name = "mini_fb/news_feed.html"
    context_object_name = "profile"
