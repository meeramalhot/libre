from django.db import models
from django.urls import reverse


class Article(models.Model):
    '''Encapsulate the idea of an Article by some author.'''

    # data attributes of a Article:
    title = models.TextField(blank=False)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)
    image_url = models.URLField(blank=True) ## new
    
    def __str__(self):
        '''Return a string representation of this Article object.'''
        return f'{self.title} by {self.author}'
    
    def get_absolute_url(self):
        '''Return the URL to display one instance of this model.'''
        return reverse('article', kwargs={'pk':self.pk})
    
