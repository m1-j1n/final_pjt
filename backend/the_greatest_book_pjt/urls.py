# the_greatest_book_pjt/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # 도서 관련 API
    path('api/v1/', include('books.urls')),

    # 회원 커스텀 기능 (회원가입, 마이페이지 등)
    path('api/v1/accounts/', include('accounts.urls')),

    # 인증 (로그인, 로그아웃, 비밀번호 변경 등)
    path('api/v1/auth/', include('dj_rest_auth.urls')),
]

# 미디어 파일 처리
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
