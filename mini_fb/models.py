from django.db import models

class Person(models.Model):
    '''Encapsulate the idea of an Article by some author.'''

    # data attributes of a Article:
    name = models.TextField(blank=False)
    au = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        '''Return a string representation of this Article object.'''
        return f'{self.name} by {self.au}'