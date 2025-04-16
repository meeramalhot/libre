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
    
    def get_reviews(self):
        revs = Review.objects.filter(profile=self)
        return revs
    
    def get_books(self):
        '''Return a QuerySet of books related to profile.'''
        books = Book.objects.filter(review__profile=self)
        return books
    
    def get_absolute_url(self):
        '''when submitting show profile form return to new profile of person'''
        return reverse('show_profile', kwargs={'pk': self.pk})
    
    def get_friends(self):
        '''function to get friends associated w a profile'''
        group1 = Friend.objects.filter(pro1 = self)
        group2 = Friend.objects.filter(pro2 = self)

        friend_group = group1 | group2
        friend_array = []
        for friend in friend_group:
            #self will be container in first or second profile
            if friend.pro1 != self:
                #if not self is not the first, append the first
                friend_array.append(friend.pro1)
            else:
                #friend will be contained in second
                friend_array.append(friend.pro2)
        
        return friend_array
    
    def add_friend(self, other):
        '''function to add friends'''

        if self == other:
             return "cannot friend self"
        
        # false if empty
        friendship = Friend.objects.filter(pro1=self, pro2=other)
        #check if already friends
        if not friendship:
            friendship = Friend.objects.filter(pro1=other, pro2=self)
            print("already friends, cannot friend")

       #if not already a friend add as friend
        if not friendship:
            add_friend = Friend(pro1=self, pro2=other)
            add_friend.save()
            print("friend added!")
    
    
    def get_friend_suggestions(self):
        '''function to get generate a list of possible new friends who are not you, or already your friend'''

        suggestions = []
        current_friends = self.get_friends()

        #add to possible friends if not already friends, or not se
        for possible in UserProfile.objects.all():
            if possible == self:
                continue
            elif possible in current_friends:
                continue
            else:
                suggestions.append(possible)

        return suggestions
    
    def get_news_feed(self):
        '''function to see all your friends status messages '''

        profiles_to_show = self.get_friends()

        # order status mesages by time stamp
        news_feed = Review.objects.filter(profile__in=profiles_to_show).order_by('-timestamp')

        return list(news_feed)

class Book(models.Model):
    title = models.TextField(blank=True)
    author = models.TextField(blank=True)
    book_cover = models.ImageField(blank=True) # an actual image
    genre = models.TextField(blank=True)
    pages = models.IntegerField(blank=True)

    def __str__(self):
        '''Return a string representation of this book object.'''
        return f'{self.title} by {self.author}'
    
    def get_reviews(self):
        '''Return a queryset of reviews related to a particular book'''
        reviews = Review.objects.filter(book=self)
        return reviews
    


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
    
