from django.urls import path
from .views import (
    CustomRegisterView,
    my_page_view,  
    user_preference_view,
    lifestyle_list,
    readingstyle_list,
    verify_password,
    public_user_profile,  
    avoided_keyword_list, 
    get_user_profile,
)

urlpatterns = [
    path('signup/', CustomRegisterView.as_view(), name='custom_signup'),
    path('mypage/', my_page_view, name='mypage'),  # 내 마이페이지 (GET, PATCH)
    path('verify-password/', verify_password, name='verify_password'),  # 수정 전 인증
    path('preference/', user_preference_view, name='user_preference'),
    path('lifestyles/', lifestyle_list, name='lifestyle_list'),
    path('readingstyles/', readingstyle_list, name='readingstyle_list'),
     path('avoided-keywords/', avoided_keyword_list, name='avoided_keywords'),
    path('<int:user_id>/profile/', public_user_profile, name='user-profile'),  # 다른 유저의 프로필 조회
    path('profile/', get_user_profile, name='my-profile'),
]
