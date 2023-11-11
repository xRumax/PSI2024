from django.db import models


class User(models.Model):
    __name__ = "user"
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    admin = models.BooleanField(default=False)


class Author(models.Model):
    __name__ = "author"
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45)
    date_of_birth = models.DateField()


class Book(models.Model):
    __name__ = "book"
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    name = models.CharField(max_length=45)
    pub = models.IntegerField()


class Review(models.Model):
    __name__ = "review"
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.FloatField()
    desc = models.CharField(max_length=45)
