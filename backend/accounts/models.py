from django.db import models
from django.contrib.auth.models import AbstractUser
from books.models import Category



class User(AbstractUser):
    
    email = None

    # 이름
    name = models.CharField(max_length=100)

    # 성별
    GENDER_CHOICES = (
        ('F', '여성'),
        ('M', '남성'),
        
    )

    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        blank=False,
        null=False,
    )

    # 나이
    age = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    # 프로필 사진
    profile_img = models.ImageField(
        upload_to='user_profile_img/',
        blank=True,
        null=True,
    )

    # 팔로잉
    followings = models.ManyToManyField(
        'self', symmetrical=False, related_name='followers'
    )

    # 설문 다 해야 회원가입 되는거임 쿠쿠
    is_signup_complete = models.BooleanField(default=False)

    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'gender', 'age']

    def __str__(self):
        return self.username

class LifestyleKeyword(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
class ReadingStyle(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preference')

    lifestyle = models.ForeignKey(LifestyleKeyword, on_delete=models.SET_NULL, null=True, blank=True)
    preferred_reading_style = models.ForeignKey(ReadingStyle, on_delete=models.SET_NULL, null=True, blank=True)

    interested_genres = models.ManyToManyField(Category, blank=True, related_name='preferred_by')
    avoided_genres = models.ManyToManyField(Category, blank=True, related_name='avoided_by')
    avoided_keywords = models.TextField(blank=True)

    weekly_avg_reading_time = models.PositiveIntegerField(blank=True, null=True)
    annual_reading_amount = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s preference"
