from rest_framework import serializers
from .models import Book, Post, Comment, BookLike, ReadingStatus, Keyword
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
    like_count = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'description', 'author', 'cover', 'category',
            'publisher', 'pub_date', 'isbn', 'customer_review_rank',
            'author_photo', 'author_info', 'like_count', 'liked'
        ]

    def get_like_count(self, obj):
        return obj.book_likes.count()

    def get_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.book_likes.filter(user=user).exists()
        return False

# 🔹 BookSimpleSerializer : 간단 데이터만 보내기 위해서
class BookSimpleSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 'cover', 'author', 'like_count', 'liked', 'category',
            'publisher', 'pub_date',]

    def get_like_count(self, obj):
        return obj.book_likes.count()

    def get_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.book_likes.filter(user=user).exists()
        return False

# 🔹 ReadingStatusSerializer : 책 상태 데이터 처리를 위해서
class ReadingStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingStatus
        fields = [
            'status',
            'start_date',
            'end_date',
            'comment',
            'progress',
            'stop_reason',
        ]

# 🔹 KeywordSerializer : 키워드 시리얼라이저

class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ['name']


# 🔹 PostCreateSerializer : 포스트 생성 시리얼라이저
class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'cover_img']
        read_only_fields = ['id']

# 🔹 PostDetailSerializer : 포스트 상세 조회 시리얼라이저
class PostDetailSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    book_id = serializers.IntegerField(source='book.id', read_only=True)
    comment_count = serializers.SerializerMethodField()
    keywords = KeywordSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'created_at', 'cover_img',
            'user', 'book_id', 'comment_count', 'keywords'
        ]

    def get_comment_count(self, obj):
        return obj.comments.count()

# 🔹 PostListSerializer : 포스트 상세 조회 시리얼라이저
class PostListSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(source='book.category.id', read_only=True)
    book_cover = serializers.ImageField(source='book.cover', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'book_cover', 'category_id', 'cover_img']

# 🔹 Comment Serializer
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # 유저 이름만 보여줄 경우

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user', 'created_at', 'updated_at', 'post']
        read_only_fields = ['user', 'created_at', 'updated_at', 'post']


# Book + 상태를 같이 보내기 위한 Serializer (마이페이지 용)
class BookWithStatusSerializer(serializers.ModelSerializer):
    book = BookSimpleSerializer(read_only=True)

    class Meta:
        model = ReadingStatus
        fields = ['book', 'status']
