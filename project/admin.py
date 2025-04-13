from django.contrib import admin

# Register your models here.

from .models import UserProfile, Review, Book, Friend
admin.site.register(UserProfile)
admin.site.register(Review)
admin.site.register(Book)
admin.site.register(Friend)