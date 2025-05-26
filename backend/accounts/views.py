from dj_rest_auth.registration.views import RegisterView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .serializers import UserProfileSerializer

from books.models import Post, Book, ReadingStatus
from .models import UserPreference, LifestyleKeyword, ReadingStyle, AvoidedKeyword, User
from .serializers import (
    CustomRegisterSerializer,
    CustomUserDetailSerializer,
    UserPreferenceSerializer,
    LifestyleKeywordSerializer,
    ReadingStyleSerializer,
    AvoidedKeywordSerializer,
)

# ✅ 커스텀 회원가입 뷰 (추가 정보 포함)
class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

# ✅ 내 마이페이지 (GET: 조회 / PATCH: 수정)
@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def my_page_view(request):
    user = request.user

    # 💡 preference가 없으면 자동 생성
    if not hasattr(user, 'preference'):
        UserPreference.objects.create(user=user)

    if request.method == 'GET':
        serializer = CustomUserDetailSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PATCH':
        serializer = CustomUserDetailSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


# ✅ 공개 프로필 조회 (유저 ID 기준)
@api_view(['GET'])
def public_user_profile(request, user_id):
    User = get_user_model()
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'detail': '사용자를 찾을 수 없습니다.'}, status=404)

    serializer = CustomUserDetailSerializer(user)
    return Response(serializer.data)


# ✅ 설문 응답 조회 & 저장 (PUT: 회원가입 마지막 단계)
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_preference_view(request):
    user = request.user
    preference, _ = UserPreference.objects.get_or_create(user=user)

    if request.method == 'GET':
        serializer = UserPreferenceSerializer(preference)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserPreferenceSerializer(preference, data=request.data)
        if serializer.is_valid():
            serializer.save()
            user.is_signup_complete = True  # ✅ 회원가입 완료 처리
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

# ✅ 피하고 싶은 키워드 목록 (다중 선택용)
@api_view(['GET'])
def avoided_keyword_list(request):
    keywords = AvoidedKeyword.objects.all()
    serializer = AvoidedKeywordSerializer(keywords, many=True)
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

# ✅ 현재 로그인 사용자 정보 저장
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    user = request.user
    return Response({
        "username": user.username,
        "email": user.email,
    })

# ✅ 팔로우 하기
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_follow(request, user_id):
    me = request.user
    you = get_object_or_404(User, id=user_id)

    if me == you:
        return Response({"detail": "자기 자신은 팔로우할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

    if you in me.followings.all():
        me.followings.remove(you)
        return Response({"followed": False})
    else:
        me.followings.add(you)
        return Response({"followed": True})

# ✅ 팔로우 여부 확인
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def follow_status(request, user_id):
    me = request.user
    you = get_object_or_404(User, id=user_id)
    is_following = you in me.followings.all()
    return Response({"is_following": is_following})

# 상대방 프로필 조회
@api_view(['GET'])
def public_user_profile(request, user_id):
    try:
        user = get_user_model().objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'detail': '사용자를 찾을 수 없습니다.'}, status=404)

    posts = Post.objects.filter(user=user)
    liked_books = Book.objects.filter(book_likes__user=user)
    reading_statuses = ReadingStatus.objects.filter(user=user)

    serializer = UserProfileSerializer(user, context={
        'request': request,
        'posts': posts,
        'liked_books': liked_books,
        'reading_statuses': reading_statuses,
    })
    return Response(serializer.data)