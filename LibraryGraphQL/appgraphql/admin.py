from django.contrib import admin
from .models import Author, Book, User, Review

# Register your models here.

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Review)
admin.site.register(User)

