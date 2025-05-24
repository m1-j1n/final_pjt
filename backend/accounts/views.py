# accounts/views.py

from dj_rest_auth.registration.views import RegisterView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

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


# ✅ 마이페이지 View
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def MyPageView(request):
    user = request.user
    serializer = CustomUserDetailSerializer(user)
    return Response(serializer.data)


# 설문 응답 View (조회 & 저장)
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def UserPreferenceView(request):
    user = request.user

    # 유저에 대한 preference가 없으면 생성
    preference, created = UserPreference.objects.get_or_create(user=user)

    if request.method == 'GET':
        serializer = UserPreferenceSerializer(preference)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserPreferenceSerializer(preference, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # 설문 완료 여부 표시
            user.is_signup_complete = True
            user.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def lifestyle_list(request):
    lifestyles = LifestyleKeyword.objects.all()
    serializer = LifestyleKeywordSerializer(lifestyles, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def readingstyle_list(request):
    reading_styles = ReadingStyle.objects.all()
    serializer = ReadingStyleSerializer(reading_styles, many=True)
    return Response(serializer.data)

# from django.http.response import JsonResponse
# from django.shortcuts import render, get_object_or_404
# from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
# from django.shortcuts import render, redirect
# from django.contrib.auth import login as auth_login
# from django.contrib.auth import logout as auth_logout
# from django.contrib.auth import update_session_auth_hash
# from django.contrib.auth import get_user_model
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import PasswordChangeForm
# from django.views.decorators.http import (
#     require_http_methods,
#     require_POST,
# )

# from .forms import CustomUserCreationForm, CustomUserChangeForm

# from django.http import JsonResponse




# @require_http_methods(["GET", "POST"])
# def login(request):
#     if request.user.is_authenticated:
#         return redirect('books:index')

#     if request.method == 'POST':
#         form = AuthenticationForm(request, request.POST)
#         if form.is_valid():
#             auth_login(request, form.get_user())
#             return redirect('books:index')
#     else:
#         form = AuthenticationForm()
#     context = {
#         'form': form,
#     }
#     return render(request, 'accounts/login.html', context)


# @require_POST
# def logout(request):
#     auth_logout(request)
#     return redirect('books:index')


# def signup(request):
#     if request.user.is_authenticated:
#         return redirect('books:index')

#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST, request.FILES)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.save()
#             selected_categories = form.cleaned_data.get('interested_genres')
#             if selected_categories:
#                 user.interested_genres.set(selected_categories)
#             auth_login(request, user)
#             return redirect('books:index')
#     else:
#         form = CustomUserCreationForm()
#     context = {
#         'form': form,
#     }
#     return render(request, 'accounts/signup.html', context)


# def profile(request, username):
#     User = get_user_model()
#     person = User.objects.get(username=username)

#     # 로그인한 유저가 person 을 팔로잉 하고 있는지
#     is_followed = False
#     if request.user.is_authenticated and request.user != person:
#         is_followed = person.followers.filter(pk=request.user.pk).exists()



#     context = {
#         'person': person,
#         'is_followed' : is_followed,
#         'follower_count': person.followers.count(),
#         'following_count' : person.followings.count(),

#     }
#     return render(request, 'accounts/profile.html', context)


# # def follow(request, user_pk):
# #     # if request.method == 'POST' and request.is_ajax():
# #     if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
# #         me = request.user
# #         target = get_object_or_404(User, pk=user_pk)

# #         if me != target:
# #             if target in me.followings.all():
# #                 me.followings.remove(target)
# #                 is_followed = False
# #             else:
# #                 me.followings.add(target)
# #                 is_followed = True
            
# #             data = {
# #                 'is_followed' : is_followed,
# #                 'follower_count' : target.followers.count(),
# #                 'following_count' : target.followings.count(),
# #             }
# #             return JsonResponse(data)
# #     return JsonResponse({'error': '잘못된 요청입니다.'}, status=400)

# @login_required
# def follow(request, user_pk):
#     User = get_user_model()
#     person = User.objects.get(pk=user_pk)
#     if person != request.user:
#         if person.followers.filter(pk=request.user.pk).exists():
#             person.followers.remove(request.user)
#             is_follow = False
#         else:
#             person.followers.add(request.user)
#             is_follow = True
#     context = {
#         # 현재 팔로우 여부
#         'is_follow': is_follow,
#         # person의 팔로워 수
#         'follower_count': person.followers.count()
#     }
#     # context 정보를 JSON으로 바꿔서 반환 -> django가 지원 import
#     return JsonResponse(context)