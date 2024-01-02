from django.contrib import admin
from .models import Author, Book, User, Review, Shop

# Register your models here.

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Review)
admin.site.register(User)
admin.site.register(Shop)

