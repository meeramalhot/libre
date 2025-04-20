from typing import Any
from django.shortcuts import render, redirect
from .models import *
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View, TemplateView, FormView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin ## NEW
from django.contrib.auth.forms import UserCreationForm ## NEW
from django.contrib.auth.models import User ## NEW
from django.contrib.auth import login # NEW
from django.contrib.auth.views import LoginView  # NEW
from .forms import *
from django.utils import timezone
import plotly
import plotly.graph_objs as go



class ShowAllProfilesView(ListView):
    '''Create a subclass of ListView to display all blog profiles.'''

    model = UserProfile # retrieve objects of type Article from the database
    template_name = 'project/show_all.html'
    context_object_name = 'profiles' # how to find the data in the template file


    def dispatch(self, request, *args, **kwargs):
        '''Override the dispatch method to add debugging information.'''

        if request.user.is_authenticated:
            print(f'ShowAllView.dispatch(): request.user={request.user}')
        else:
            print(f'ShowAllView.dispatch(): not logged in.')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=self.request.user)
            except UserProfile.DoesNotExist:
                profile = None
            
            context['profile'] = profile
        return context


class ProfileDetailView(DetailView):
    model = UserProfile
    template_name = 'project/prof_detail.html'
    context_object_name = 'profiles'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:

            profile = UserProfile.objects.get(user=self.request.user)
            context['profile'] = profile

        return context

class CreateProfileView(CreateView):
    '''A view to handle creation of a new profile.
    (1) display the HTML form to user (GET)
    (2) process the form submission and store the new Article object (POST)
    '''

    form_class = MakeProfileForm
    template_name = 'project/make_profile.html'
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        # add to context
        context['user_creation_form'] = UserCreationForm()
        return context
    
    def form_valid(self, form):
        user_form = UserCreationForm(self.request.POST)
        if user_form.is_valid():
                new_user = user_form.save()
                login(self.request, new_user)
                form.instance.user = new_user
                form.instance.date_joined = timezone.now()
                
                return super().form_valid(form)
        else:
                    print("invalid form!")
                    return self.form_invalid(form)
        
    def get_login_url(self) -> str:
        return reverse('login')


class DeleteReviewView(LoginRequiredMixin, DeleteView):
    '''Allows u to delete a status message'''

    template_name = "project/delete_review.html"
    model = Review
    context_object_name = 'review'

    def get_success_url(self):
        '''Return a the URL to which we should be directed after the delete.'''

        # get the pk for this sm
        pk = self.kwargs.get('pk')
        review = Review.objects.get(pk=pk)
        
        # find the review to which this Profile is related by FK
        profile = review.profile
        
        # reverse to show the article page
        return reverse('show_profile', kwargs={'pk':profile.pk})
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    

class AddFriendView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):

        # dont use pk to get friend_one
        friend_one = UserProfile.objects.get(user=request.user)
        # Retrieve the other user's pk from the URL parameter 'other_pk'
        other_pk = self.kwargs['other_pk']
        friend_two = UserProfile.objects.get(pk=other_pk)

        friend_one.add_friend(friend_two)
        
        return redirect('show_profile', pk=friend_one.pk)
        
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    
    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)
    

class ShowFriendSuggestionsView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = "project/friend_suggest.html"
    context_object_name = "profile"

        
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    
    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)
    
class ShowFeedView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = "project/feed.html"
    context_object_name = "profile"

        
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    
    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)


class UpdateReviewView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = UpdateReviewForm
    template_name = 'project/update_review_form.html'
    context_object_name = 'review'

    def get_queryset(self):
        user_profile = UserProfile.objects.get(user=self.request.user)
        return Review.objects.filter(profile=user_profile)

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})
    

class BookUploadView(LoginRequiredMixin, CreateView):
    '''A view to handle creation of a new Comment on an Article.'''

    form_class = UploadBookForm
    template_name = "project/book_upload.html"

    def get_success_url(self):
        '''Provide a URL to redirect to after creating a new status message.'''
        return reverse('review_upload')
    
    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''
        context = super().get_context_data(**kwargs)

        profile = UserProfile.objects.get(user=self.request.user)
        context['profile'] = profile
        return context
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    
    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)

    def form_valid(self, form):
        '''This method handles the form submission
        '''
        print(form.cleaned_data)
        user = self.request.user
        print(f"CreateStatusMessage user={user}")

        # delegate the work to the superclass method form_valid:
        return super().form_valid(form)
    

class ReviewUploadView(LoginRequiredMixin, CreateView):
    '''A view to handle creation of a new Comment on an Article.'''

    form_class = ReviewForm
    template_name = "project/review_upload.html"

    def get_success_url(self):
        '''Provide a URL to redirect to after creating a new status message.'''
        profile = UserProfile.objects.get(user=self.request.user)
        return reverse('show_profile', kwargs={'pk': profile.pk})
    
    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''
        context = super().get_context_data(**kwargs)

        profile = UserProfile.objects.get(user=self.request.user)
        context['profile'] = profile
        return context
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    
    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)

    def form_valid(self, form):
        '''This method handles the form submission and sa{% url 'show_profile' profile.pk %}ves the new object to the Django database.
        We need to add the foreign key (of the Article) to the Comment object before saving it to the database
        '''
        print(form.cleaned_data)
        #dont add to db, manually add some info
        review = form.save(commit=False)

        review.profile = UserProfile.objects.get(user=self.request.user)
        review.date_finished = timezone.now()
        #add to db
        review.save()
        return super().form_valid(form)


class UserAnalyticsView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'project/analytics.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = context['profile']

        # get books reviewed by this profile
        books = Book.objects.filter(review__profile=profile)

        book_counts=0
        book_pages_sum=0
        genre_counts = {}
        for book in books:
            #used later for stats
            book_counts+=1
            book_pages_sum += book.pages
            genre = book.genre
            #use dict to add up counts
            genre_counts[genre] = genre_counts.get(genre, 0) + 1

        labels = list(genre_counts.keys())
        values = [genre_counts[genre] for genre in labels]

        pie_chart = go.Pie(labels=labels, values=values)
        title_text = f"Your Genre Breakdown"

        genre_pie = plotly.offline.plot({"data": [pie_chart], 
                                         "layout_title_text": title_text,
                                         }, 
                                         auto_open=False, 
                                         output_type="div")

        context['genre_pie'] = genre_pie

        reviews = Review.objects.filter(profile=profile)

        #check books per year
        year_counts = {}
        for review in reviews:
            if review.date_finished:
                year = review.date_finished.year
                year_counts[year] = year_counts.get(year, 0) + 1

        sorted_years = sorted(year_counts)
        x = sorted_years
        y = [year_counts[year] for year in sorted_years]

        x = [str(x) for x in sorted_years]


        bar_chart = go.Bar(x=x, y=y)
        title_text = f"Books Read Per Year"

        books_year = plotly.offline.plot({"data": [bar_chart], 
                                         "layout_title_text": title_text,
                                         }, 
                                         auto_open=False, 
                                         output_type="div")

        context['books_year'] = books_year
        
        average = book_pages_sum/book_counts
        #get average with trailing of only 2
        context['average'] = float(f"{average:.2f}")

        #get top read books
        total_review_count = Review.objects.filter(profile=profile).count() 
        context['total_review_count'] = total_review_count
        if (total_review_count >= 3):
            rev_one = Review.objects.filter(profile=profile).order_by("-rating", "-date_finished")[0]
            context['rev_one'] = rev_one.book
            rev_two = Review.objects.filter(profile=profile).order_by("-rating", "-date_finished")[1]
            context['rev_two'] = rev_two.book
            rev_three = Review.objects.filter(profile=profile).order_by("-rating", "-date_finished")[2]
            context['rev_three'] = rev_three.book





        return context
    

