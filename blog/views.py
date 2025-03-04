from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Article
from .forms import CreateArticleForm, CreateCommentForm
from django.urls import reverse
import random
# Create your views here.

class ShowAllView(ListView):
    '''Define a view class to show all blog Articles'''

    model = Article
    template_name = "blog/show_all.html"
    context_object_name = "articles" #naming convention -- whenever we are creating a list view we are going to show many objects, we want to use a plural name similar to the model name.
    #going to conatin very instances of the article


#detail view displays a single instance of one model

class ArticleView(DetailView):
    '''Display a single article'''

    model = Article
    template_name = "blog/article.html"
    context_object_name = "article" # note singular variable name

class RandomArticleView(DetailView):
    '''Display a single article selected at random'''

    model = Article
    template_name = "blog/article.html"
    context_object_name = "article" # note singular variable name

    #methods

    def get_object(self):
        '''return one instance of the Article object selected at random.'''

        all_articles = Article.objects.all()
        article = random.choice(all_articles)
        return article
    
# define a subclass of CreateView to handle creation of Article objects

class CreateArticleView(CreateView):
    '''A view to handle creation of a new article.
    (1) display the HTML form to user (GET)
    (2) process the form submission and store the new Article object (POST)
    '''

    form_class = CreateArticleForm
    template_name = "blog/create_article_form.html"

    def form_valid(self, form):
        '''
        Handle the form submission to create a new Article object.
        '''
        print(f'CreateArticleView: form.cleaned_data={form.cleaned_data}')

		# delegate work to the superclass version of this method
        return super().form_valid(form)

class CreateCommentView(CreateView):
    '''A view to handle creation of a new Comment on an Article.'''

    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"

    def get_success_url(self):
        '''Provide a URL to redirect to after creating a new Comment.'''
        # return reverse('show_all')
        #retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        #call reverse to generate the URL for this Article
        return reverse('article', kwargs={'pk':pk})
    
    def get_context_data(self):
        '''Return the dictionary of context variables for use in the template'''

        #calling the superclass method
        context = super().get_context_data()

        # find/add the article to the context data
        # retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk)

        # add this article into the context dictionary:
        context ['article'] = article
        return context 
    

    def form_valid(self, form):
        '''This method handles the form submission and saves the new object to the Django database.
        We need to add the foreign key (of the Article) to the Comment object before saving it to the database
        '''

        print(form.cleaned_data)
        #retrieve the PK from the URL pattern
        pk = self.kwargs['pk']
        article = Article.objects.get(pk=pk)
        # attach this article to the comment
        form.instance.article = article # set the FK

        # delegate the work to the superclass method form_valid:
        return super().form_valid(form)