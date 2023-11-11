from rest_framework import serializers
from datetime import datetime
from .models import Book, Review, User, Author


class BookSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    author_id = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())
    name = serializers.CharField(max_length=200)
    pub = serializers.IntegerField()

    class Meta:
        model = Book
        fields = ["id", "author_id", "name", "pub"]

    def validate_id(self, value):
        if value < 0 and isinstance(value, int):
            raise serializers.ValidationError("ID is invalid")
        return value

    def validate_name(self, value):
        if len(value) < 2 or len(value) > 200 or not isinstance(value, str):
            raise serializers.ValidationError("Name is too short or too long")
        return value

    def validate_pub(self, value):
        if value > datetime.now().year or not isinstance(value, int):
            raise serializers.ValidationError("Date is in the future")
        return value

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class ReviewSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    book_id = serializers.IntegerField()
    rating = serializers.FloatField()
    desc = serializers.CharField(max_length=200)

    class Meta:
        model = Review
        fields = ["id", "user_id", "book_id", "rating", "desc"]

    def valitate_id(self, value):
        if value < 0 and isinstance(value, int):
            raise serializers.ValidationError("ID is invalid")
        return value

    def valitate_user_id(self, value):
        if value < 0 and isinstance(value, int):
            raise serializers.ValidationError("User ID is invalid")
        return value

    def valitate_book_id(self, value):
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


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=200)
    password = serializers.CharField(max_length=200)
    admin = serializers.BooleanField()

    class Meta:
        model = User
        fields = ["id", "name", "password", "admin"]

    def valitate_id(self, value):
        if value < 0 and isinstance(value, int):
            raise serializers.ValidationError("ID is invalid")
        return value

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


class AuthorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
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
