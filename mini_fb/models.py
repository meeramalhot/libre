'''
author: meera malhotra
date: 2/26
filename: models.py
description: profile models for db
'''

from django.db import models
from django.urls import reverse


class Profile(models.Model):
    '''Encapsulate profile info for a person.'''

    # data attributes of a Article:
    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.TextField(blank=False)
    #image_url = models.URLField(blank=True) ## new
    image_file = models.ImageField(blank=True) # an actual image


    
    def __str__(self):
        '''Return a string representation of this Article object.'''
        return f'{self.first_name} {self.last_name}'
    
    def get_status_messages(self):
        '''Return a QuerySet of statuses related to profile.'''
        statuses = StatusMessage.objects.filter(profile=self)
        return statuses
    
    def get_absolute_url(self):
        '''when submitting show profile form return to new profile aof person'''
        return reverse('show_profile', kwargs={'pk': self.pk})

    

class StatusMessage(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    message = models.TextField(blank=False)


    def __str__(self):
        '''Return a string representation of this status message'''
        return f'{self.message}'


