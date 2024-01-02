from django.db import models

class User(models.Model):
    name = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    admin = models.BooleanField(default=False)


class Author(models.Model):
    name = models.CharField(max_length=45)
    date_of_birth = models.DateField()


class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    name = models.CharField(max_length=45)
    pub = models.IntegerField()


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.FloatField()
    desc = models.CharField(max_length=255)

class Shop(models.Model):
    name = models.CharField(max_length=255)
    adress = models.CharField(max_length=550)
    email = models.CharField(max_length=255)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
