from rest_framework import serializers
from .models import Book, Thread, Comment
from accounts.models import Category
from django.contrib.auth import get_user_model

User = get_user_model()

# 🔹 Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


# 🔹 Book Serializer
class BookSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)  

    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'description',
            'author',
            'cover',
            'category',
            'publisher',
            'pub_date',
            'isbn',
            'customer_review_rank',
            'author_photo',
            'author_info',
        ]


# 🔹 Thread Serializer
class ThreadSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # username 보여주기
    book = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Thread
        fields = ['id', 'title', 'content', 'cover_img', 'user', 'book', 'created_at']


# 🔹 Comment Serializer
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # username

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'thread', 'created_at']
