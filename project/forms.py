from django import forms
from .models import *

class MakeProfileForm(forms.ModelForm):
    '''A form to add a Profile to the database'''

    class Meta:
        '''associate this form with a model from our database'''
        model = UserProfile
        fields = ['first_name', 'last_name', 'email', 'pfp']


#https://docs.djangoproject.com/en/5.2/topics/forms/
#https://docs.djangoproject.com/en/5.2/ref/forms/widgets/


class UploadBookForm(forms.ModelForm):
    '''A form to update info abt a book in the database'''
    #https://stackoverflow.com/questions/604266/django-set-default-form-values

    class Meta:
        model = Book
        fields = ['title', 'author', 'book_cover', 'genre', 'pages'] 

class ReviewForm(forms.ModelForm):
    '''A form to add a review to the database'''

    #https://docs.djangoproject.com/en/3.0/ref/models/fields/#django.db.models.Field.choices
    #ensures that there's a drop down of rating from 1-5 stars

    stars = [(i, str(i)) for i in range(1, 6)]

    #set 1-5 as choices
    rating = forms.ChoiceField(choices=stars, widget=forms.Select)

    class Meta:
        model = Review
        fields = ['review', 'rating', 'book']


class UpdateReviewForm(forms.ModelForm):
    '''A form to update a review'''

    class Meta:
        model = Review
        fields = ['review', 'rating', 'date_finished']
