from django.urls import path
from . import views
from django.contrib import admin
from .views import BookList, ReviewList, UserList

urlpatterns = [
    path("admin/", admin.site.urls),
    path("",views.index, name="index"),
    path("api/books", BookList.as_view()),
    path("api/reviews", ReviewList.as_view()),
    path("api/users", UserList.as_view()),
]
