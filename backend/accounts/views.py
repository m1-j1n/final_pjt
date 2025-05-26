from dj_rest_auth.registration.views import RegisterView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import get_user_model  # ✅ 다른 사람 프로필 조회용
from .serializers import (
    CustomRegisterSerializer,
    CustomUserDetailSerializer,
    UserPreferenceSerializer,
)
from .models import UserPreference
from accounts.models import LifestyleKeyword, ReadingStyle
from accounts.serializers import LifestyleKeywordSerializer, ReadingStyleSerializer


# ✅ 회원가입 View (커스텀 serializer 사용)
class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer


# ✅ 내 마이페이지 View (GET, PATCH)
@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def MyPageView(request):
    user = request.user

    if request.method == 'GET':
        serializer = CustomUserDetailSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        serializer = CustomUserDetailSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


# ✅ 다른 사람 마이페이지 View (GET만)
@api_view(['GET'])
def public_user_profile(request, user_id):
    User = get_user_model()
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'detail': '사용자를 찾을 수 없습니다.'}, status=404)

    serializer = CustomUserDetailSerializer(user)
    return Response(serializer.data)


# ✅ 설문 응답 View
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def UserPreferenceView(request):
    user = request.user
    preference, created = UserPreference.objects.get_or_create(user=user)

    if request.method == 'GET':
        serializer = UserPreferenceSerializer(preference)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserPreferenceSerializer(preference, data=request.data)
        if serializer.is_valid():
            serializer.save()
            user.is_signup_complete = True
            user.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ 라이프스타일 키워드 목록
@api_view(['GET'])
def lifestyle_list(request):
    lifestyles = LifestyleKeyword.objects.all()
    serializer = LifestyleKeywordSerializer(lifestyles, many=True)
    return Response(serializer.data)


# ✅ 독서 스타일 목록
@api_view(['GET'])
def readingstyle_list(request):
    reading_styles = ReadingStyle.objects.all()
    serializer = ReadingStyleSerializer(reading_styles, many=True)
    return Response(serializer.data)


# ✅ 비밀번호 인증
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_password(request):
    user = request.user
    password = request.data.get('password')

    if not password or not user.check_password(password):
        return Response({'detail': '비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)

    return Response({'detail': '비밀번호 인증 성공'}, status=status.HTTP_200_OK)
