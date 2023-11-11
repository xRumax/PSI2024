from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from .models import Book, Review, User, Author
from .serialisers import (
    BookSerializer,
    ReviewSerializer,
    UserSerializer,
    AuthorSerializer,
)
from django.http import Http404


class BookList(APIView):
    """
    List all books, or create a new book.
    """

    def get(self, request, format=None):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            author_id = serializer.validated_data.get("author_id")
            try:
                author = Author.objects.get(id=author_id)
            except Author.DoesNotExist:
                return Response(
                    {"message": "Author does not exist"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            new_book = serializer.save(author_id=author)

            return Response(serializer.data(), status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewList(APIView):
    """
    List all reviews, or create a new review.
    """

    def get(self, request, format=None):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserList(APIView):
    """
    List all users, or create a new user.
    """

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthorList(APIView):
    """
    List all authors, or create a new author.
    """

    def get(self, request, format=None):
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# get book by id
class BookDetail(APIView):
    """
    Retrieve, update or delete a book instance.
    """

    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        book = self.get_object(pk)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Book updated successfully"}, status=status.HTTP_200_OK
            )

    def delete(self, request, pk, format=None):
        book = self.get_object(pk)
        book.delete()
        return Response(
            {"message": "Book deleted successfully"}, status=status.HTTP_200_OK
        )


class AuthorDetail(APIView):
    """
    Retrieve, update or delete a author instance.
    """

    def get_object(self, pk):
        try:
            return Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        author = self.get_object(pk)
        serializer = AuthorSerializer(author, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Author updated successfully"}, status=status.HTTP_200_OK
            )

    def delete(self, request, pk, format=None):
        author = self.get_object(pk)
        author.delete()
        return Response(
            {"message": "Author deleted successfully"}, status=status.HTTP_200_OK
        )


class ReviewDetail(APIView):
    """
    Retrieve, update or delete a review instance.
    """

    def get_object(self, pk):
        try:
            return Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        review = self.get_object(pk)
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Review updated successfully"}, status=status.HTTP_200_OK
            )

    def delete(self, request, pk, format=None):
        review = self.get_object(pk)
        review.delete()
        return Response(
            {"message": "Review deleted successfully"}, status=status.HTTP_200_OK
        )


class UserDetail(APIView):
    """
    Retrieve, update or delete a user instance.
    """

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User updated successfully"}, status=status.HTTP_200_OK
            )

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(
            {"message": "User deleted successfully"}, status=status.HTTP_200_OK
        )
