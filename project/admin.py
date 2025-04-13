from django.contrib import admin

# Register your models here.

from .models import Profile, Review, Book, Friend
admin.site.register(Profile)
admin.site.register(Review)
admin.site.register(Book)
admin.site.register(Friend)