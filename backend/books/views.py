from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import (
    require_safe,
    require_POST,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from rest_framework import status
from rest_framework.parsers import MultiPartParser


from accounts.models import Category
from .models import Book, Post, Comment, BookLike, Book, ReadingStatus
from .utils import get_random_image_file, generate_recommendation_summary
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from .serializers import BookSerializer, CategorySerializer, PostDetailSerializer, PostCreateSerializer, PostListSerializer, BookSimpleSerializer, CommentSerializer, ReadingStatusSerializer

### 도서 ###
# 책 전체 조회
@api_view(['GET'])
@permission_classes([AllowAny])
def book_list(request):
    paginator = PageNumberPagination()
    paginator.page_size = 10

    books = Book.objects.all().order_by('id')
    # books = Book.objects.all()
    result_page = paginator.paginate_queryset(books, request)
    serializer = BookSerializer(result_page, many=True, context={'request': request})
    return paginator.get_paginated_response(serializer.data)

# 카테고리 조회
@api_view(['GET'])
def category_list(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)

# 장르별 필터링 - 책
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 12  # 페이지당 도서 수

@api_view(['GET'])
def filter_books_by_category(request, category_id):
    books = Book.objects.filter(category__id=category_id)
    paginator = StandardResultsSetPagination()
    paginated_qs = paginator.paginate_queryset(books, request)
    serializer = BookSimpleSerializer(paginated_qs, many=True, context={'request': request})
    return paginator.get_paginated_response(serializer.data)

# 장르별 필터링 - 포스트
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
    
    serializer = BookSerializer(book, context={'request': request})
    return Response(serializer.data)

# 도서 검색
@api_view(['GET'])
def book_search(request):
    query = request.query_params.get('query', '').strip()
    if not query:
        return Response({'message': '검색어를 입력해 주세요'}, status=status.HTTP_400_BAD_REQUEST)
    keywords = query.split()
    # Q 객체 조합: 각 단어가 title, author, publisher 중 하나에라도 포함되도록 함
    q = Q()
    for word in keywords:
        q &= (
            Q(title__icontains=word) |
            Q(author__icontains=word) |
            Q(publisher__icontains=word)
        )
    books = Book.objects.filter(q)
    if not books.exists():
        return Response({'message': '검색 결과가 없습니다'}, status=status.HTTP_200_OK)
    serializer = BookSerializer(books, many=True, context={'request': request})
    return Response(serializer.data)

# 도서 상태 기록
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reading_status_create_or_update(request, book_id):
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        return Response({'error': '책을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    # 기존 상태가 있다면 수정, 없으면 생성
    instance, created = ReadingStatus.objects.get_or_create(user=request.user, book=book)

    serializer = ReadingStatusSerializer(instance, data=request.data, partial=True)
    # if serializer.is_valid():
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED)
    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED)
    else:
        print(serializer.errors)  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 포스트 생성
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser])
def post_create(request, book_pk):
    try:
        book = Book.objects.get(pk=book_pk)
    except Book.DoesNotExist:
        return Response({'error': '책을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    data = request.data.copy()
    files = request.FILES.copy()

    # 커버 이미지가 없는 경우 랜덤 이미지 할당
    if 'cover_img' not in files:
        random_image = get_random_image_file()
        if random_image:
            files['cover_img'] = random_image

    serializer = PostCreateSerializer(data=data)
    if serializer.is_valid():
        post = serializer.save(book=book, user=request.user)
        return Response(PostCreateSerializer(post).data, status=status.HTTP_201_CREATED)
    
    print(serializer.errors)
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

# 포스트 수정
@api_view(['PATCH'])
# @permission_classes([IsAuthenticated])
def post_update(request, book_pk, post_pk):
    try:
        post = Post.objects.get(pk=post_pk, book_id=book_pk)
    except Post.DoesNotExist:
        return Response({'error': '게시글을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    # if post.user != request.user:
    #     raise PermissionDenied('수정 권한이 없습니다.')

    serializer = PostCreateSerializer(post, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 포스트 삭제
@api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
def post_delete(request, book_pk, post_pk):
    try:
        post = Post.objects.get(pk=post_pk, book_id=book_pk)
    except Post.DoesNotExist:
        return Response({'error': '존재하지 않는 게시글입니다.'}, status=status.HTTP_404_NOT_FOUND)

    # 글을 작성한 사용자만 삭제 가능
    # if post.user != request.user:
    #     return Response({'error': '삭제 권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

    post.delete()
    return Response({'success': True}, status=status.HTTP_204_NO_CONTENT)

# 도서 좋아요 처리
@api_view(['POST'])
@permission_classes([IsAuthenticated])  
def book_like_toggle(request, book_pk):
    book = get_object_or_404(Book, pk=book_pk)
    user = request.user

    like, created = BookLike.objects.get_or_create(user=user, book=book)
    
    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    serializer = BookSimpleSerializer(book, context={'request': request})
    return Response({
        'liked': liked,
        'like_count': book.book_likes.count(),
        'book': serializer.data
    })

# 도서 상태 (콘텐츠 기반) 추천
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommend_similar_books(request):
    user = request.user

    reading_books = ReadingStatus.objects.filter(user=user, status='reading').select_related('book')
    if not reading_books.exists():
        reading_books = ReadingStatus.objects.filter(user=user, status='done').select_related('book')
    if not reading_books.exists():
        return Response({'books': [], 'summary': ''}, status=200)

    user_books = [rs.book.title for rs in reading_books]
    categories = [rs.book.category for rs in reading_books]
    read_ids = [rs.book.id for rs in reading_books]

    recommended_books = Book.objects.filter(category__in=categories).exclude(id__in=read_ids).distinct()[:10]

    # GPT 추천 요약 생성
    summary = generate_recommendation_summary(user_books, recommended_books)

    from .serializers import BookSimpleSerializer
    serialized_books = BookSimpleSerializer(recommended_books, many=True, context={'request': request})

    return Response({
        'summary': summary,
        'books': serialized_books.data,
    })


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


# 포스트 댓글 생성
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user, post=post)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 포스트 댓글 리스트 조회
@api_view(['GET'])
def comments_list(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    comments = post.comments.all().order_by('-created_at') 
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)

# 포스트 댓글 삭제
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_comment(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)

    if request.user != comment.user:
        return Response({'error': '댓글 작성자만 삭제할 수 있습니다.'}, status=status.HTTP_403_FORBIDDEN)

    comment.delete()
    return Response({'message': '댓글이 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)

