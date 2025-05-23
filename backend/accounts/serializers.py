from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from books.models import Category

print("✅ CustomRegisterSerializer 모듈 로드됨")  # 이게 뜨는지 확인!


User = get_user_model()

class CustomRegisterSerializer(RegisterSerializer):
    name = serializers.CharField()
    gender = serializers.CharField(allow_null=True, required=False)
    age = serializers.IntegerField(allow_null=True, required=False)
    weekly_avg_reading_time = serializers.IntegerField(allow_null=True, required=False)
    annual_reading_amount = serializers.IntegerField(allow_null=True, required=False)
    profile_img = serializers.ImageField(required=False)
    interested_genres = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), many=True, required=False
    )

    def save(self, request):
        print('호출됨!!!')
        user = super().save(request)

        user.name = self.validated_data.get('name')
        user.gender = self.validated_data.get('gender')
        user.age = self.validated_data.get('age')
        user.weekly_avg_reading_time = self.validated_data.get('weekly_avg_reading_time')
        user.annual_reading_amount = self.validated_data.get('annual_reading_amount')
        user.profile_img = self.validated_data.get('profile_img')
        user.save()

        genres = self.validated_data.get('interested_genres')
        if genres:
            user.interested_genres.set(genres)

        return user
