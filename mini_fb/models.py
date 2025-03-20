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
    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    city = models.TextField(blank=True)
    email = models.TextField(blank=True)
    image_url = models.URLField(blank=True)

    def __str__(self):
        '''Return a string representation of this Article object.'''
        return f'{self.first_name} {self.last_name}'
    
    def get_status_messages(self):
        '''Return a QuerySet of statuses related to profile.'''
        statuses = StatusMessage.objects.filter(profile=self)
        return statuses
    
    def get_absolute_url(self):
        '''when submitting show profile form return to new profile of person'''
        return reverse('show_profile', kwargs={'pk': self.pk})
    
    def get_friends(self):
        '''function to get friends associated w a profile'''

        group1 = Friend.objects.filter(profile1 = self)
        group2 = Friend.objects.filter(profile2 = self)
        #print(group1)

        friend_group = group1 | group2
        #print(friend_group)
        friend_array = []
        for friend in friend_group:
            #self will be container in first or second profile
            if friend.profile1 != self:
                #if not self is not the first, append the first
                friend_array.append(friend.profile1)
            else:
                #friend will be contained in second
                friend_array.append(friend.profile2)
        
        #print(friend_array)

        return friend_array
    
    def add_friend(self, other):
        '''function to add friends'''

        if self == other:
             return "cannot friend self"
        
        # false if empty
        friendship = Friend.objects.filter(profile1=self, profile2=other)
        #check if already friends
        if not friendship:
            friendship = Friend.objects.filter(profile1=other, profile2=self)
            print("already friends, cannot friend")

       
        if not friendship:
            add_friend = Friend(profile1=self, profile2=other)
            add_friend.save()
            print("friend added!")


    def get_friend_suggestions(self):
       no_self = Friend.objects.exclude(pk=self.pk)
       friend_one = Friend.objects.filter(profile1=self)
       friend_two = Friend.objects.filter(profile2=self)
       cant_friend = friend_one or friend_two or no_self

       suggestions = Profile.objects.all().exclude(cant_friend) 

       return suggestions[:3]


class StatusMessage(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    message = models.TextField(blank=False)

    def __str__(self):
        '''Return a string representation of this status message'''
        return f'{self.message}'
    
    def get_images(self):
        '''return all images associated with status message'''
        images = Image.objects.filter(statusimage__status_message=self)

        return images


class Image(models.Model):
    image_file = models.ImageField(blank=True) # an actual image
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    caption = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)


    def __str__(self):
        '''Return a string representation of this image object.'''
        return f'{self.caption}'
    

class StatusImage(models.Model):
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)

    def __str__(self):
        '''Return a string representation of this status image object.'''
        return f'{self.status_message}'

class Friend(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    profile1 = models.ForeignKey(Profile, related_name="profile1", on_delete=models.CASCADE)
    profile2 = models.ForeignKey(Profile, related_name="profile2", on_delete=models.CASCADE)

    def __str__(self):
        '''Return a string representation of friend object.'''
        return f'{self.profile1} & {self.profile2}'
    
