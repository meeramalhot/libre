from django.shortcuts import render
from .models import Article
from django.views.generic import ListView, DetailView, CreateView
import random
from .forms import CreateArticleForm ## new


class ShowAllView(ListView):
    '''Create a subclass of ListView to display all blog articles.'''

    model = Article # retrieve objects of type Article from the database
    template_name = 'blog/show_all.html'
    context_object_name = 'articles' # how to find the data in the template file

## add this view class:
class ArticleView(DetailView):
    '''Show the details for one article.'''
    model = Article
    template_name = 'blog/article.html' ## reusing same template!!
    context_object_name = 'article'


class RandomArticleView(DetailView):
    '''Show the details for one article.'''
    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article'

    # pick one article at random:
    def get_object(self):
        '''Return one Article object chosen at random.'''

        all_articles = Article.objects.all()
        return random.choice(all_articles)
    

# define a subclass of CreateView to handle creation of Article objects
class CreateArticleView(CreateView):
    '''A view to handle creation of a new Article.
    (1) display the HTML form to user (GET)
    (2) process the form submission and store the new Article object (POST)
    '''

    form_class = CreateArticleForm
    template_name = "blog/create_article_form.html"