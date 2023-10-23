# example model for user
from django.db import models


class User(models.Model):
    __name__ = "user"
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    admin = models.BooleanField(default=False)


class Book(models.Model):
    __name__ = "book"
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    author = models.CharField(max_length=45)
    pub = models.DateField()


class Review(models.Model):
    __name__ = "review"
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.FloatField(max_value=5.0, min_value=0.0)
    desc = models.CharField(max_length=45)
