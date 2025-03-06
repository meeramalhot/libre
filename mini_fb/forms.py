from django import forms
from .models import Profile, StatusMessage, Image, StatusImage

class CreateProfileForm(forms.ModelForm):
    '''A form to add a Profile to the database'''

    class Meta:
        '''associate this form with a model from our database'''
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email', 'image_url']

class CreateStatusMessageForm(forms.ModelForm):
    '''A status message to add a Profile to the database'''

    class Meta:
           model = StatusMessage
           fields = ['message']

class UpdateProfileForm(forms.ModelForm):
    '''A form to update a Profile's details, excluding the first and last name.'''

    class Meta:
        model = Profile
        fields = ['city', 'email', 'image_url']

