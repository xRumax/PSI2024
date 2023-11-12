from rest_framework import serializers
from datetime import datetime
from .models import Book, Review, User, Author


class AuthorSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=45)
    date_of_birth = serializers.DateField()

    class Meta:
        model = Author
        fields = ["id", "name", "date_of_birth"]

    def valitate_id(self, value):
        if value < 0 and isinstance(value, int):
            raise serializers.ValidationError("ID is invalid")
        return value

    def valitate_name(self, value):
        if len(value) < 2 and len(value) > 200 and isinstance(value, str):
            raise serializers.ValidationError("Name is too short")
        return value

    def date_of_birth(self, value):
        if value > datetime.date.today() and isinstance(value, datetime.date):
            raise serializers.ValidationError("Date is in the future")
        return value

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only = True)
    author_id = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(),source ="author", write_only=True)
    name = serializers.CharField(max_length=45)
    pub = serializers.IntegerField()


    class Meta:
        model = Book
        fields = ["id", "author", "name", "pub", "author_id"]

    def validate_id(self, value):
        if value < 0 and isinstance(value, int):
            raise serializers.ValidationError("ID is invalid")
        return value

    def validate_name(self, value):
        if len(value) < 2 or len(value) > 45 or not isinstance(value, str):
            raise serializers.ValidationError("Name is too short or too long")
        return value

    def validate_pub(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Year is in the future")
        return value

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    
class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=200)
    admin = serializers.BooleanField()

    class Meta:
        model = User
        fields = ["id", "name", "password", "admin"]


    def valitate_name(self, value):
        if len(value) < 2 and len(value) > 200 and isinstance(value, str):
            raise serializers.ValidationError("Name is too short")
        return value

    def valitate_password(self, value):
        if len(value) < 2 and len(value) > 200 and isinstance(value, str):
            raise serializers.ValidationError("Password is too short")
        return value

    def valitate_admin(self, value):
        if isinstance(value, bool):
            raise serializers.ValidationError("Admin is invalid")
        return value

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='name')
    book = serializers.SlugRelatedField(queryset=Book.objects.all(), slug_field='name')
    author = serializers.SlugRelatedField(queryset=Author.objects.all(), slug_field='name')
    rating = serializers.FloatField()
    desc = serializers.CharField(max_length=200)

    class Meta:
        model = Review
        fields = ["id", "user", "book", "author", "rating", "desc" ]

    def valitate_id(self, value):
        if value < 0 and isinstance(value, int):
            raise serializers.ValidationError("ID is invalid")
        return value

    def valitate_user(self, value):
        if value < 0 and isinstance(value, int):
            raise serializers.ValidationError("User ID is invalid")
        return value

    def valitate_book(self, value):
        if value < 0 and isinstance(value, int):
            raise serializers.ValidationError("Book ID is invalid")
        return value

    def valitate_rating(self, value):
        if value < 0 and value > 5 and isinstance(value, float):
            raise serializers.ValidationError("Rating is invalid")
        return value

    def valitate_desc(self, value):
        if len(value) < 2 and len(value) > 200 and isinstance(value, str):
            raise serializers.ValidationError("Description is invalid")
        return value

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


