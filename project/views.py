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
from django.http import HttpResponseRedirect

class HomeView(TemplateView):
    '''basic view to just render homepage.'''

    template_name = 'project/home.html'

    def get_context_data(self, **kwargs):
        #this is for the profile info in navbar
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:

            profile = UserProfile.objects.get(user=self.request.user)
            context['profile'] = profile

        return context

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
        #this is for the profile info in navbar
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=self.request.user)
            except UserProfile.DoesNotExist:
                profile = None
            
            context['profile'] = profile
        return context


class ProfileDetailView(DetailView):
    '''view for a specific profile'''

    model = UserProfile
    template_name = 'project/prof_detail.html'
    context_object_name = 'profiles'

    def get_context_data(self, **kwargs):
        #this is for the profile info in navbar and if they can do operations like review upload delete etc
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:

            profile = UserProfile.objects.get(user=self.request.user)
            context['profile'] = profile

        return context

class CreateProfileView(CreateView):
    '''A view to handle creation of a new profile.
    (1) display the HTML form to user (GET)
    (2) process the form submission and store the new profile object (POST)
    '''

    form_class = MakeProfileForm
    template_name = 'project/make_profile.html'
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        # add to context
        context['user_creation_form'] = UserCreationForm()
        return context
    
    def form_valid(self, form):
        """add user form and check if valid, if valid set time user joined and log them in"""
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
    '''Allows u to delete a review'''

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
    """logic to add a friend, interacts w db model"""
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
    """provides info to show possible friends"""
    model = UserProfile
    template_name = "project/friend_suggest.html"
    context_object_name = "profile"

        
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    
    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)
    
class ShowFeedView(LoginRequiredMixin, DetailView):
    """provides info for user's review feed"""
    model = UserProfile
    template_name = "project/feed.html"
    context_object_name = "profile"

        
    def get_login_url(self) -> str:
        '''return the URL required for login if not loggied in'''
        return reverse('login')
    
    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)


class UpdateReviewView(LoginRequiredMixin, UpdateView):
    """update review using the form_class"""
    model = Review
    form_class = UpdateReviewForm
    template_name = 'project/update_review_form.html'
    context_object_name = 'review'

    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''
        context = super().get_context_data(**kwargs)

        profile = UserProfile.objects.get(user=self.request.user)
        context['profile'] = profile
        return context

    #get reviews of one logged in user
    def get_queryset(self):
        user_profile = UserProfile.objects.get(user=self.request.user)
        return Review.objects.filter(profile=user_profile)

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})
    

class BookUploadView(LoginRequiredMixin, CreateView):
    '''A view to handle creation of a new book'''

    form_class = UploadBookForm
    template_name = "project/book_upload.html"

    def get_success_url(self):
        '''Provide a URL to redirect to after creating a new book'''
        #add book object so review form can autopopulate
        return reverse('review_upload') + f'?book={self.object.pk}'
    
    def get_login_url(self) -> str:
        '''return the URL required for login'''
        return reverse('login')
    
    def get_context_data(self, **kwargs):
        '''Return the dictionary of context variables for use in the template.'''
        context = super().get_context_data(**kwargs)

        profile = UserProfile.objects.get(user=self.request.user)
        context['profile'] = profile
        return context
    
    def get_object(self):
        """get logged in user"""
        return UserProfile.objects.get(user=self.request.user)

    def form_valid(self, form):
        '''This method handles the form submission
        '''
        print(form.cleaned_data)
        title  = form.cleaned_data["title"].strip()
        author = form.cleaned_data["author"].strip()
        
        #https://www.w3schools.com/django/django_ref_field_lookups.php
        #same as exact, but case-insensitive
        #get the first dupicate so we can pass in a book for redirect

        #check if this book already exists, if it does, autopopulate with the prexisting book 
        #do not add duplicate to db
        duplicate = Book.objects.filter(title__icontains=title, author__iexact=author).first()
        if duplicate:
            print("hit duplicate case")
            url = reverse("review_upload") + f"?book={duplicate.pk}"
            return HttpResponseRedirect(url)

        # delegate the work to the superclass method form_valid:
        return super().form_valid(form)
    

class ReviewUploadView(LoginRequiredMixin, CreateView):
    '''A view to handle creation of a new review.'''

    form_class = ReviewForm
    template_name = "project/review_upload.html"

    def get_success_url(self):
        '''Provide a URL to redirect to after creating a new status message.'''
        profile = UserProfile.objects.get(user=self.request.user)
        return reverse('show_profile',  kwargs={'pk': profile.pk})
    
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
        """get logged in user"""
        return UserProfile.objects.get(user=self.request.user)
    
    #set the inital value of the book to be what the user just uploaded in review form
    def get_initial(self):
        initial = super().get_initial()
        book_id = self.request.GET.get("book")
        #make sure it exists
        if book_id and Book.objects.filter(pk=book_id).exists():
            initial["book"] = book_id
        return initial

    def form_valid(self, form):
        '''This method handles the form submission and saves the new object to the Django database.
        We need to add the foreign key profile to the review object and set the date before saving it to the database
        '''
        print(form.cleaned_data)
        #dont add to db, manually add some info
        review = form.save(commit=False)

        review.profile = UserProfile.objects.get(user=self.request.user)
        #set date finished
        review.date_finished = timezone.now()
        #add to db
        review.save()
        return super().form_valid(form)


class UserAnalyticsView(LoginRequiredMixin, DetailView):
    """A view to display a users personal reading analyticd"""
    model = UserProfile
    template_name = 'project/analytics.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = context['profile']

        # get books reviewed by this profile
        books = Book.objects.filter(review__profile=profile)

        #get counts per genre, as well as total book counts and total summation of pages for 
        #average page count
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

        #THIS IS FOR GENRE PIE CHART - DISPLAYS A CHART OF WHAT PERCENT OF BOOKS USER READ IN WHAT GENRE
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

        #REVIEWS PER YEAR COUNT
        #get reviews associated w logged in profile
        reviews = Review.objects.filter(profile=profile)

        #these are for calculating the average rating
        rating_sum = 0
        rating_count = 0
        #check books per year
        year_counts = {}
        for review in reviews:
            rating_sum += review.rating 
            rating_count += 1
            if review.date_finished:
                #add to dict count of book finished per year
                year = review.date_finished.year
                year_counts[year] = year_counts.get(year, 0) + 1
        
        #calculate the average rating and pass in as a context variable, rounding to 2 dec points pout
        avg_rating = rating_sum / rating_count
        context['average_rating'] = float(f"{avg_rating:.2f}")

        sorted_years = sorted(year_counts)
        x = sorted_years
        y = [year_counts[year] for year in sorted_years]
        #standardize x axis so we dont get decimal years
        x = [str(x) for x in sorted_years]

        #bar chart passed in as obkect of books read per year
        bar_chart = go.Bar(x=x, y=y)
        title_text = f"Books Read Per Year"

        books_year = plotly.offline.plot({"data": [bar_chart], 
                                         "layout_title_text": title_text,
                                         }, 
                                         auto_open=False, 
                                         output_type="div")

        context['books_year'] = books_year
        
        #get average amount of pages read and pass in as context variable
        average = book_pages_sum/book_counts
        #get average with trailing of only 2
        context['average'] = float(f"{average:.2f}")

        #get top read books
        total_review_count = Review.objects.filter(profile=profile).count() 
        context['total_review_count'] = total_review_count
        #check if more than three books otherwise indexing error
        if (total_review_count >= 3):
            rev_one = Review.objects.filter(profile=profile).order_by("-rating", "-date_finished")[0]
            context['rev_one'] = rev_one.book
            rev_two = Review.objects.filter(profile=profile).order_by("-rating", "-date_finished")[1]
            context['rev_two'] = rev_two.book
            rev_three = Review.objects.filter(profile=profile).order_by("-rating", "-date_finished")[2]
            context['rev_three'] = rev_three.book


        return context

class ShowAllBooksView(ListView):
    ''' display all books '''

    model = Book
    template_name = 'project/books.html'
    context_object_name = 'books' # how to find the data in the template file

    def get_context_data(self, **kwargs):
        #get logged in user as context for navbar
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:

            profile = UserProfile.objects.get(user=self.request.user)
            context['profile'] = profile

        return context


class BookDetailView(DetailView):
    """specific book page for each book"""
    model = Book
    template_name = 'project/book.html'
    context_object_name = 'book'


    def get_context_data(self, **kwargs):
        #get logged in user as context for navbar
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:

            profile = UserProfile.objects.get(user=self.request.user)
            context['profile'] = profile

        return context
    

class SuggestionView(LoginRequiredMixin, ListView):
    """get suggestions based on readers genres and what friends are reading"""
    model = Book
    template_name = 'project/get_suggestions.html'
    context_object_name = 'book'

    def get_genres(self):
        """return a qs of all genres this user has read"""
        profile = UserProfile.objects.get(user=self.request.user)
        books= Book.objects.filter(review__profile=profile) 

        #for if no reviews
        if not books.exists():
            return [], []  
        
        #get all genres this reader reads to filter on later
        genre_counts = {}

        for book in books:
            genre = book.genre
            genre_counts[genre] = genre_counts.get(genre, 0) + 1

        all_genres = list(genre_counts.keys())
        #top_genres = []

        # #check if all genres is longer than three to get top three
        # if len(all_genres) <= 3:
        #     top_genres = all_genres
        # else:
        #     # sorting values in descending order
        #     output = dict(sorted(genre_counts.items(), key=lambda item: item[1], reverse=True))

        #     for genre in output:
        #         top_genres.append(genre)
        #         #only get the top three
        #         if len(top_genres) == 3:
        #             break

        return all_genres


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            #get logged in user
            profile = UserProfile.objects.get(user=self.request.user)
            context['profile'] = profile
            
            #get suggestions from what friends read not including your reads
            suggestions = Book.objects.filter(review__profile__in=profile.get_friends()).exclude(review__profile=profile).distinct()
            
            #get reccomendations based on the genres you read
            all_genres = self.get_genres()
            genre_books = Book.objects.filter(genre__in=all_genres).exclude(review__profile=profile).distinct()

            #slice by 5 all of the query sets so doesnt give too many reccommendations

            #top recs are what your friends read and genres you like
            top_recs = suggestions & genre_books
            if top_recs.count() > 5:
                top_recs = top_recs[:5]

            context["top_recs"] = top_recs

            #cannot slice before anding
            if genre_books.count() > 5:
                genre_books =  genre_books[:5]
            context["genre_books"] = genre_books

            if suggestions.count() > 5:
                suggestions = suggestions[:5]
            context["suggestions"] = suggestions

        return context
