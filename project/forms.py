from django import forms
from .models import *

class MakeProfileForm(forms.ModelForm):
    '''A form to add a Profile to the database'''

    class Meta:
        '''associate this form with a model from our database'''
        model = UserProfile
        fields = ['first_name', 'last_name', 'email', 'pfp']

class BookSelectionForm(forms.ModelForm):
    '''A form to add a book to the database'''

    class Meta:
        model = Book
        fields = ['title', 'author', 'book_cover', 'genre', 'pages'] 

class UpdateBookForm(forms.ModelForm):
    '''A form to update info abt a book in the database'''

    class Meta:
        model = Book
        fields = ['title', 'author', 'book_cover', 'genre', 'pages'] 

class ReviewForm(forms.ModelForm):
    '''A form to add a review to the database'''

    class Meta:
        model = Review
        fields = ['review', 'rating', 'date_finished']

class UpdateReviewForm(forms.ModelForm):
    '''A form to update a review'''

    class Meta:
        model = Review
        fields = ['review', 'rating', 'date_finished']
