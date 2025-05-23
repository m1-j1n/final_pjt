from django.urls import path
from . import views


app_name = "books"
urlpatterns = [
    # 도서
    path('categories/', views.category_list, name='category_list'),
    path('books/', views.book_list, name='book_list'),
    # path('books/filter/', views.filter_category, name='filter_category'),
    path('books/<int:book_pk>/', views.detail, name='book_detail'),
    path('books/category/<int:category_id>/', views.filter_books_by_category, name='filter_books_by_category'),

    # 포스트
    path('books/<int:book_pk>/posts/create/', views.post_create, name='post_create'),
    path('books/<int:book_pk>/posts/<int:post_pk>/', views.post_detail, name='post_detail'),
    path('books/<int:book_pk>/posts/<int:post_pk>/update/', views.post_update, name='post_update'),
    path('books/<int:book_pk>/posts/<int:post_pk>/delete/', views.post_delete, name='post_delete'),
    path('posts/category/<int:category_id>/', views.filter_posts_by_category, name='filter_posts_by_category'),

    path('posts/', views.post_list, name='post_list'),



    # 좋아요
    path('books/<int:book_pk>/threads/<int:thread_pk>/likes/', views.likes, name='likes'),

    # 댓글
    path('books/<int:book_pk>/threads/<int:thread_pk>/comments/create/', views.create_comment, name='create_comment'),
    path('books/<int:book_pk>/comments/<int:comment_pk>/delete/', views.delete_comment, name='delete_comment'),
]