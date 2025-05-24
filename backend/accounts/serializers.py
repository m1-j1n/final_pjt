from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from books.models import Category
from .models import UserPreference, LifestyleKeyword, ReadingStyle

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
# 2. 설문 응답용
# -------------------------------
class UserPreferenceSerializer(serializers.ModelSerializer):
    interested_genres = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), many=True, required=False
    )
    avoided_genres = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), many=True, required=False
    )

    class Meta:
        model = UserPreference
        fields = [
            'lifestyle',
            'preferred_reading_style',
            'interested_genres',
            'avoided_genres',
            'avoided_keywords',
            'weekly_avg_reading_time',
            'annual_reading_amount',
        ]

# -------------------------------
# 3. 마이페이지용
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

class UserPreferenceDetailSerializer(serializers.ModelSerializer):
    interested_genres = CategorySerializer(many=True)
    avoided_genres = CategorySerializer(many=True)
    lifestyle = LifestyleKeywordSerializer()
    preferred_reading_style = ReadingStyleSerializer()

    class Meta:
        model = UserPreference
        fields = [
            'lifestyle',
            'preferred_reading_style',
            'interested_genres',
            'avoided_genres',
            'avoided_keywords',
            'weekly_avg_reading_time',
            'annual_reading_amount',
        ]

class CustomUserDetailSerializer(serializers.ModelSerializer):
    preference = UserPreferenceDetailSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            'username',  # 로그인용 ID
            'name',      # 사용자 이름
            'gender',
            'age',
            'profile_img',
            'preference',
            'is_signup_complete',
        ]
