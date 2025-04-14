'''
author: meera malhotra
date: 4/9
filename: models.py
description: profile models for db
'''

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class UserProfile(models.Model):
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
    
        
    def get_books(self):
        '''Return a QuerySet of statuses related to profile.'''
        books = Book.objects.filter(profile=self)
        return books
    
class Book(models.Model):
    title = models.TextField(blank=True)
    author = models.TextField(blank=True)
    book_cover = models.ImageField(blank=True) # an actual image
    genre = models.TextField(blank=True)
    pages = models.IntegerField(blank=True)
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        '''Return a string representation of this book object.'''
        return f'{self.title} by {self.author}'
    
class Review(models.Model):
    review = models.TextField(blank=True)
    rating = models.IntegerField(blank=True)
    date_finished = models.DateTimeField(blank=True)
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        '''Return a string representation of this book object.'''
        return f'{self.profile} on {self.book}'


class Friend(models.Model):
    pro1 = models.ForeignKey(UserProfile, related_name="pro1", on_delete=models.CASCADE)
    pro2 = models.ForeignKey(UserProfile, related_name="pro2", on_delete=models.CASCADE)

    def __str__(self):
        '''Return a string representation of friend object.'''
        return f'{self.pro1} & {self.pro2}'
    
