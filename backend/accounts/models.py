from django.db import models
from django.contrib.auth.models import AbstractUser
from books.models import Category

# 🔹 사용자 모델
class User(AbstractUser):
    email = None  # 이메일은 사용하지 않음

    name = models.CharField(max_length=100)

    GENDER_CHOICES = (
        ('F', '여성'),
        ('M', '남성'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    age = models.PositiveIntegerField(null=True, blank=True)

    profile_img = models.ImageField(
        upload_to='user_profile_img/',
        null=True, blank=True,
    )

    followings = models.ManyToManyField(
        'self', symmetrical=False, related_name='followers'
    )

    is_signup_complete = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'gender', 'age']

    def __str__(self):
        return self.username


# 🔹 키워드 모델들
class LifestyleKeyword(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class ReadingStyle(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class AvoidedKeyword(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preference')

    lifestyles = models.ManyToManyField(LifestyleKeyword, blank=True)
    preferred_reading_styles = models.ManyToManyField(ReadingStyle, blank=True)
    interested_genres = models.ManyToManyField(Category, related_name='preferred_by', blank=True)  
    avoided_genres = models.ManyToManyField(Category, related_name='avoided_by', blank=True)
    avoided_keywords = models.ManyToManyField(AvoidedKeyword, blank=True)

    weekly_avg_reading_time = models.PositiveIntegerField(blank=True, null=True)
    annual_reading_amount = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s preference"

