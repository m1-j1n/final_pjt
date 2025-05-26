from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from books.models import Category
from books.serializers import PostListSerializer, BookSimpleSerializer, LikedOrReadBookSerializer
from books.models import ReadingStatus
from .models import (
    UserPreference,
    LifestyleKeyword,
    ReadingStyle,
    AvoidedKeyword,
)

User = get_user_model()

# -------------------------------
# 1. 회원가입용
# -------------------------------
class CustomRegisterSerializer(RegisterSerializer):
    email = None  # ❌ 이메일 제거

    username = serializers.CharField()  # 로그인용 ID
    name = serializers.CharField()      # 사용자 이름
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    gender = serializers.CharField()
    age = serializers.IntegerField()
    profile_img = serializers.ImageField(required=False)

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username'),
            'password1': self.validated_data.get('password1'),
            'name': self.validated_data.get('name'),
            'gender': self.validated_data.get('gender'),
            'age': self.validated_data.get('age'),
            'profile_img': self.validated_data.get('profile_img'),
        }

    def save(self, request):
        user = super().save(request)
        user.name = self.cleaned_data.get('name')
        user.gender = self.cleaned_data.get('gender')
        user.age = self.cleaned_data.get('age')
        user.profile_img = self.cleaned_data.get('profile_img')
        user.save()
        return user

# -------------------------------
# 2. 설문 저장/수정용
# -------------------------------
class UserPreferenceSerializer(serializers.ModelSerializer):
    lifestyles = serializers.PrimaryKeyRelatedField(
        queryset=LifestyleKeyword.objects.all(), many=True
    )
    preferred_reading_styles = serializers.PrimaryKeyRelatedField(
        queryset=ReadingStyle.objects.all(), many=True
    )
    interested_genres = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), many=True
    )
    avoided_genres = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), many=True
    )
    avoided_keywords = serializers.PrimaryKeyRelatedField(
        queryset=AvoidedKeyword.objects.all(), many=True
    )

    class Meta:
        model = UserPreference
        fields = [
            'lifestyles',
            'preferred_reading_styles',
            'interested_genres',
            'avoided_genres',
            'avoided_keywords',
            'weekly_avg_reading_time',
            'annual_reading_amount',
        ]

# -------------------------------
# 3. 마이페이지 조회용 (상세 정보 포함)
# -------------------------------
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class LifestyleKeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = LifestyleKeyword
        fields = ['id', 'name']

class ReadingStyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingStyle
        fields = ['id', 'name']

class AvoidedKeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvoidedKeyword
        fields = ['id', 'name']

class UserPreferenceDetailSerializer(serializers.ModelSerializer):
    lifestyles = LifestyleKeywordSerializer(many=True)
    preferred_reading_styles = ReadingStyleSerializer(many=True)
    interested_genres = CategorySerializer(many=True)
    avoided_genres = CategorySerializer(many=True)
    avoided_keywords = AvoidedKeywordSerializer(many=True)

    class Meta:
        model = UserPreference
        fields = [
            'lifestyles',
            'preferred_reading_styles',
            'interested_genres',
            'avoided_genres',
            'avoided_keywords',
            'weekly_avg_reading_time',
            'annual_reading_amount',
        ]

class CustomUserDetailSerializer(serializers.ModelSerializer):
    preference = UserPreferenceDetailSerializer(read_only=True)
    followers_count = serializers.SerializerMethodField()
    followings_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'username',
            'name',
            'gender',
            'age',
            'profile_img',
            'preference',
            'is_signup_complete',
            'followers_count', 
            'followings_count',
        ]

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_followings_count(self, obj):
        return obj.followings.count()
    

User = get_user_model()
class UserProfileSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField()
    books = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    followings_count = serializers.SerializerMethodField()
    preference = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'name', 'profile_img',
            'gender', 'age',
            'preference',
            'posts', 'books',
            'followers_count', 'followings_count',
        ]

    def get_preference(self, obj):
        if hasattr(obj, 'preference') and obj.preference:
            return UserPreferenceDetailSerializer(obj.preference).data
        return None

    def get_posts(self, obj):
        posts = self.context.get('posts', [])
        return PostListSerializer(posts, many=True, context=self.context).data

    def get_books(self, obj):
        liked_books = self.context.get('liked_books', [])
        reading_statuses = self.context.get('reading_statuses', [])
        status_dict = {rs.book.id: rs.status for rs in reading_statuses}
        return LikedOrReadBookSerializer(
            liked_books, many=True,
            context={**self.context, 'status_dict': status_dict}
        ).data

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_followings_count(self, obj):
        return obj.followings.count()