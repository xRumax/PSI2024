from django.db import models

class User(models.Model):
    id = models.IntegerField(primary_key=True)
    user_name = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    admin = models.BooleanField(False)


class Book(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=45)
    author = models.CharField(max_length=45)
    pub = models.DateField()

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    desc = models.CharField(max_length=45)
    rating = models.FloatField(max=5.0, min=0.0)
    

