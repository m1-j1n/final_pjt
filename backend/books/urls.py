from django.urls import path
from . import views


app_name = "books"
urlpatterns = [
    ### 도서 ###
    path('categories/', views.category_list, name='category_list'),
    path('books/', views.book_list, name='book_list'),
    # path('books/filter/', views.filter_category, name='filter_category'),
    path('books/<int:book_pk>/', views.detail, name='book_detail'),
    path('books/category/<int:category_id>/', views.filter_books_by_category, name='filter_books_by_category'),
    path('books/<int:book_pk>/like/', views.book_like_toggle, name='book_like_toggle'),
    # 독서 상태 기록
    path('books/<int:book_id>/reading-status/', views.reading_status_create_or_update, name='reading_status_create_or_update'),
    # 추천
    path('recommend/content-based/', views.recommend_similar_books, name='recommend_similar_books'),
    path('recommend/dropped-books/', views.dropped_books_summary, name='dropped-books-summary'),

    # 검색
    path('books/search/', views.book_search, name='book_search'),
    path('books/<int:book_pk>/posts/list/', views.book_related_posts, name='book_related_posts'),
    

    ### 포스트 ###
    path('posts/', views.post_list, name='post_list'),
    path('books/<int:book_pk>/posts/create/', views.post_create, name='post_create'),
    path('books/<int:book_pk>/posts/<int:post_pk>/', views.post_detail, name='post_detail'),
    path('books/<int:book_pk>/posts/<int:post_pk>/update/', views.post_update, name='post_update'),
    path('books/<int:book_pk>/posts/<int:post_pk>/delete/', views.post_delete, name='post_delete'),
    path('posts/category/<int:category_id>/', views.filter_posts_by_category, name='filter_posts_by_category'),
    path('posts/mine/', views.my_posts, name='my_posts'), # 마이페이지에 가져올 포스트들



    # 댓글
    path('posts/<int:post_pk>/comments/', views.comments_list, name='comments_list'),
    path('posts/<int:post_pk>/comments/create/', views.create_comment, name='create_comment'),
    path('comments/<int:comment_pk>/delete/', views.delete_comment, name='delete_comment'),

    # # 좋아요
    # path('books/<int:book_pk>/threads/<int:thread_pk>/likes/', views.likes, name='likes'),
]