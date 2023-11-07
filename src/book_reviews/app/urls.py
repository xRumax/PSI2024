"""
URL configuration for book_reviews project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.http import HttpResponseNotFound


def index(request):
    return HttpResponse("Hello, world")


def error_404_view(request, exception):
    return HttpResponseNotFound("Error 404, page not found")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index),
    path("api/", include("book_reviews.urls")),
    path("<path:path>", error_404_view),
]
