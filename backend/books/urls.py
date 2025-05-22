from django.urls import path
from . import views


app_name = "books"
urlpatterns = [
    # 도서
    path('categories/', views.category_list, name='category_list'),
    path('books/', views.book_list, name='book_list'),
    path('books/filter/', views.filter_category, name='filter_category'),
    path('books/<int:book_pk>/', views.detail, name='book_detail'),

    # 쓰레드
    path('books/<int:book_pk>/threads/create/', views.thread_create, name='thread_create'),
    path('books/<int:book_pk>/threads/<int:thread_pk>/', views.thread_detail, name='thread_detail'),
    path('books/<int:book_pk>/threads/<int:thread_pk>/update/', views.thread_update, name='thread_update'),
    path('books/<int:book_pk>/threads/<int:thread_pk>/delete/', views.thread_delete, name='thread_delete'),

    # 좋아요
    path('books/<int:book_pk>/threads/<int:thread_pk>/likes/', views.likes, name='likes'),

    # 댓글
    path('books/<int:book_pk>/threads/<int:thread_pk>/comments/create/', views.create_comment, name='create_comment'),
    path('books/<int:book_pk>/comments/<int:comment_pk>/delete/', views.delete_comment, name='delete_comment'),
]