from django.db import models
from django.urls import reverse
# Create your models here.
#define data models here

class Article(models.Model):
    '''Encapsulate the date of a blog Article by an author'''

    #define the data attributes of the Article object

    title = models.TextField(blank=True)
    author = models.TextField(blank=True)
    text = models.TextField(blank=True)
    published = models.DateTimeField(auto_now = True) #will set the published time automatically to the published time
    #image_url = models.URLField(blank=True)
    image_file = models.ImageField(blank=True) # an actual image

    

    def __str__(self): 
        '''return a string representation of this model instance'''
        return f'{self.title} by {self.author}'
    
    def get_absolute_url(self):
        '''Return a URL to display one instance of this object.'''
        return reverse('article', kwargs={'pk': self.pk})
    
    def get_all_comments(self):
        '''Return a QuerySet of comments about this article.'''
        comments = Comment.objects.filter(article=self)
        return comments
    
class Comment(models.Model):
    '''Encapsulate the idea of a comment about an Article'''
    
    # data attributes of the Comment:

    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return a string representation of this Comment'''
        return f'{self.text}'