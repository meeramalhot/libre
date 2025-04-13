'''
author: meera malhotra
date: 4/9
filename: models.py
description: profile models for db
'''

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Profile(models.Model):
    '''Encapsulate profile info for a person.'''

    # data attributes of a profile:
    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    email = models.TextField(blank=True)
    date_joined = models.DateTimeField(blank=True)
    pfp = models.ImageField(blank=True) # an actual image
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        '''Return a string representation of this profile object.'''
        return f'{self.first_name} {self.last_name}'
    
class Book(models.Model):
    title = models.TextField(blank=True)
    author = models.TextField(blank=True)
    book_cover = models.ImageField(blank=True) # an actual image
    genre = models.TextField(blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        '''Return a string representation of this book object.'''
        return f'{self.title} by {self.author}'
    
class Review(models.Model):
    review = models.TextField(blank=True)
    rating = models.IntegerField(blank=True)
    date_finished = models.DateTimeField(blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        '''Return a string representation of this book object.'''
        return f'{self.profile} on {self.book}'


class Friend(models.Model):
    profile1 = models.ForeignKey(Profile, related_name="profile1", on_delete=models.CASCADE)
    profile2 = models.ForeignKey(Profile, related_name="profile2", on_delete=models.CASCADE)

    def __str__(self):
        '''Return a string representation of friend object.'''
        return f'{self.profile1} & {self.profile2}'
    
