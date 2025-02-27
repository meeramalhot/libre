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
    image_url = models.URLField(blank=True) ## new

    
    def __str__(self):
        '''Return a string representation of this Article object.'''
        return f'{self.first_name} {self.last_name}'
    
    def get_status_messages(self):
        '''Return a QuerySet of comments about this article.'''
        statuses = StatusMessage.objects.filter(profile=self)
        return statuses
    

class StatusMessage(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    message = models.TextField(blank=False)


    def __str__(self):
        '''Return a string representation of this Comment'''
        return f'{self.message}'


