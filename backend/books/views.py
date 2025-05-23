from django.http import JsonResponse
from django.views.decorators.http import (
    require_http_methods,
    require_safe,
    require_POST,
)
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from accounts.models import Category
from .models import Book, Post, Comment
from .forms import PostForm, CommentForm
from .utils import (
    generate_image_with_openai,
)
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from .serializers import BookSerializer, CategorySerializer, PostDetailSerializer, PostCreateSerializer, PostListSerializer, BookSimpleSerializer

# 책 전체 조회
@api_view(['GET'])
def book_list(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

# 카테고리 조회
@api_view(['GET'])
def category_list(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

# 장르별 필터링 - 책
@api_view(['GET'])
def filter_books_by_category(request, category_id):
    books = Book.objects.filter(category__id=category_id)
    serializer = BookSimpleSerializer(books, many=True)
    return Response({'books': serializer.data})

# 장르별 필터링 - 리뷰
@api_view(['GET'])
def filter_posts_by_category(request, category_id):
    posts = Post.objects.filter(book__category__id=category_id)
    serializer = PostListSerializer(posts, many=True)
    return Response({'posts': serializer.data})

# 도서 상세 정보
@require_safe
@api_view(['GET'])
def detail(request, book_pk):
    try:
        book = Book.objects.get(pk=book_pk)
    except Book.DoesNotExist:
        return Response({'error': '도서를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = BookSerializer(book)
    return Response(serializer.data)


# 포스트 생성
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def post_create(request, book_pk):
    try:
        book = Book.objects.get(pk=book_pk)
    except Book.DoesNotExist:
        return Response({'error': '책을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = PostCreateSerializer(data=request.data)
    if serializer.is_valid():
        user = request.user if request.user.is_authenticated else None
        post = serializer.save(book=book, user=user)

        # OpenAI 이미지 생성
        generated_image_path = generate_image_with_openai(post.title, post.content, book.title, book.author)
        if generated_image_path:
            post.cover_img = generated_image_path
            post.save()

        return Response(PostCreateSerializer(post).data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# 포스트 상세
@api_view(['GET'])
# @permission_classes([IsAuthenticated])  ← 로그인 제한이 필요하면 유지
def post_detail(request, book_pk, post_pk):
    try:
        post = Post.objects.get(pk=post_pk, book_id=book_pk)
    except Post.DoesNotExist:
        return Response({'error': '포스트를 찾을 수 없습니다.'}, status=404)

    serializer = PostDetailSerializer(post)
    return Response(serializer.data)

# 포스트 목록
@api_view(['GET'])
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    serializer = PostDetailSerializer(posts, many=True)
    return Response(serializer.data)

# 카테고리 불러오기
def categories_list(request):
    return

# 쓰레드 수정
@login_required
@require_http_methods(["POST"])
def thread_update(request, book_pk, thread_pk):
    thread = Thread.objects.get(pk=thread_pk)
    if thread.user != request.user:
        raise PermissionDenied

    form = ThreadForm(request.POST, request.FILES, instance=thread)
    if form.is_valid():
        form.save()
        return JsonResponse({'success': True})
    return JsonResponse({'error': '수정 실패'}, status=400)

# 쓰레드 삭제
@login_required
@require_POST
def thread_delete(request, book_pk, thread_pk):
    thread = Thread.objects.get(pk=thread_pk)
    if thread.user == request.user:
        thread.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'error': '삭제 권한 없음'}, status=403)


# 쓰레드 좋아요 처리
@login_required
@require_POST
def likes(request, book_pk, thread_pk):
    thread = Thread.objects.get(pk=thread_pk)
    user = request.user

    if thread.likes.filter(pk=user.pk).exists():
        thread.likes.remove(user)
        liked = False
    else:
        thread.likes.add(user)
        liked = True

    return JsonResponse({
        'liked': liked,
        'like_count': thread.likes.count(),
    })


# 쓰레드 댓글 생성
@login_required
def create_comment(request, book_pk, thread_pk):
    thread = Thread.objects.get(pk=thread_pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.thread = thread
        comment.user = request.user
        comment_form.save()
        return JsonResponse({
            'id': comment.id,
            'content': comment.content,
            'username': comment.user.username,
            'is_owner': comment.user == request.user
        })
    return JsonResponse({'error': 'Invalid form'}, status=400)


# 쓰레드 댓글 삭제
@login_required
def delete_comment(request, book_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'error': '권한 없음'}, status=403)