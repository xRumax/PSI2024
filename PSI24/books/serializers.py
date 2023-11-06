from rest_framework import serializers
from .models import *

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(primary_key=True)
    user_name = serializers.CharField(max_length=45)
    password = serializers.CharField(max_length=45)
    admin = serializers.BooleanField(default=False)
        
    def create(self, validated_data):
        return User(**validated_data)
    
    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.user_name = validated_data.get('user_name', instance.user_name)
        instance.password = validated_data.get('password', instance.password)
        instance.admin = validated_data.get('admin', instance.admin)
        instance.save()
        return instance        
    
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Hasło jest za krótkie! Powinno składać się z conajmniej 8 znaków!")
        return value
    
class BookSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Book
        fields = ['id', 'name', 'author','pub']

    def create(self, validated_data):
        return Book(**validated_data)
    
    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.name = validated_data.get('name', instance.name)
        instance.author = validated_data.get('author', instance.author)
        instance.pub = validated_data.get('pub', instance.pub)
        instance.save()
        return instance
    
class ReviewSerializer(serializers.Serializer):
    id = serializers.AutoField(primary_key=True)
    book = serializers.ForeignKey(Book, on_delete=models.CASCADE)
    creator = serializers.ForeignKey(User, on_delete=models.CASCADE)
    desc = serializers.CharField(max_length=45)
    rating = serializers.FloatField(max=5.0, min=0.0)

    def create(self, validated_data):
        return Review(**validated_data)
    
    def update(self, instance, validated_data):
        instance.id = validated_data.get('id', instance.id)
        instance.book = validated_data.get('book', instance.book)
        instance.creator = validated_data.get('create', instance.create)
        instance.desc = validated_data.get('desc', instance.desc)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.save()
        return instance

    def validate_rating(self, value):
        if value > 5.0 or value < 0.0:
            raise serializers.ValidationError("Ocena powinna być w przedziale od 0 do 5")
        return value
    