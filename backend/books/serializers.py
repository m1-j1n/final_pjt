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
            'stop_date',
            'stop_reason',
        ]

# 🔹 StoppedBookSerializer : 키워드 시리얼라이저
class StoppedBookSerializer(serializers.ModelSerializer):
    book_id = serializers.IntegerField(source='book.id', read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)
    book_cover = serializers.URLField(source='book.cover', read_only=True) 
    stop_reason = serializers.CharField()

    class Meta:
        model = ReadingStatus
        fields = ['book_id', 'book_title', 'book_cover', 'stop_reason']

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
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    book_id = serializers.IntegerField(source='book.id', read_only=True)
    comment_count = serializers.SerializerMethodField()
    keywords = KeywordSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'created_at', 'cover_img',
            'user', 'user_id', 'book_id', 'comment_count', 'keywords'
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

# 🔹 LikedOrReadBookSerializer
class LikedOrReadBookSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    liked = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'description', 'cover', 'author',
            'publisher', 'pub_date', 'category',
            'like_count', 'liked', 'status',
        ]

    def get_like_count(self, obj):
        return obj.book_likes.count()

    def get_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.book_likes.filter(user=user).exists()
        return False

    def get_status(self, obj):
        # 읽은 책이라면 context에 status_dict가 들어 있음
        status_dict = self.context.get('status_dict', {})
        return status_dict.get(obj.id)  # 없으면 None
