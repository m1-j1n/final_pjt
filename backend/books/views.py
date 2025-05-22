from django.http import JsonResponse
from django.views.decorators.http import (
    require_http_methods,
    require_safe,
    require_POST,
)
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from accounts.models import Category
from .models import Book, Thread, Comment
from .forms import ThreadForm, CommentForm
from .utils import (
    generate_image_with_openai,
)
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from .serializers import BookSerializer, CategorySerializer

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

# 장르별 필터링
def filter_category(request):
    # ajax 호출: ?category=장르이름
    category_name = request.GET.get('category')
    if category_name:
        qs = Book.objects.filter(category__name=category_name)
    else:
        qs = Book.objects.all()

    # json 직렬화
    data = [{
        'id'         : b.pk,
        'title'      : b.title,
        'description': b.description[:180],
        'cover'      : b.cover or '',
    } for b in qs]

    return JsonResponse({'books': data})


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


# 쓰레드 생성
@login_required
@require_http_methods(["POST"])
def thread_create(request, book_pk):
    book = Book.objects.get(pk=book_pk)
    form = ThreadForm(request.POST, request.FILES)
    if form.is_valid():
        thread = form.save(commit=False)
        thread.book = book
        thread.user = request.user
        thread.save()

        generated_image_path = generate_image_with_openai(thread.title, thread.content, book.title, book.author)
        if generated_image_path:
            thread.cover_img = generated_image_path
            thread.save()

        return JsonResponse({
            "id": thread.id,
            "title": thread.title,
            "content": thread.content,
            "cover_img": thread.cover_img,
        })
    return JsonResponse({'error': '유효하지 않은 입력입니다.'}, status=400)


# 쓰레드 상세
@login_required
@require_safe
def thread_detail(request, book_pk, thread_pk):
    try:
        thread = Thread.objects.get(pk=thread_pk, book_id=book_pk)
        return JsonResponse({
            "id": thread.id,
            "title": thread.title,
            "content": thread.content,
            "user": thread.user.username,
            "book_id": thread.book.id,
            "cover_img": thread.cover_img,
            "created_at": thread.created_at,
        })
    except Thread.DoesNotExist:
        return JsonResponse({'error': '쓰레드를 찾을 수 없습니다.'}, status=404)


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