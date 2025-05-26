import datetime
from django.db import models
from django.conf import settings

# 카테고리 테이블
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# 도서 테이블
class Book(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name='books'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    isbn = models.CharField(max_length=20)
    cover = models.URLField()  
    publisher = models.CharField(max_length=100)
    pub_date = models.DateField()
    author = models.CharField(max_length=100)
    author_info = models.TextField()
    author_photo = models.URLField()  
    customer_review_rank = models.FloatField()
    subTitle = models.CharField(max_length=100)

    def __str__(self):
        return self.title

# 도서 좋아요 테이블
class BookLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book') 

class ReadingStatus(models.Model):
    STATUS_CHOICES = [
        ('done', '완독'),
        ('reading', '읽는 중'),
        ('stop', '중단'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    
    # 공통
    start_date = models.DateField(null=True, blank=True)

    # 완독일 때
    end_date = models.DateField(null=True, blank=True)
    comment = models.TextField(blank=True)

    # 읽는 중일 때 - 0~100%
    progress = models.PositiveIntegerField(null=True, blank=True)  

    # 중단일 때
    stop_date = models.DateField(null=True, blank=True)
    stop_reason = models.TextField(blank=True)
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.user.username} - {self.book.title} ({self.status})"
    
# 키워드 테이블
class Keyword(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# 포스트 테이블
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    reading_date = models.DateField(default=datetime.date.today)
    cover_img = models.ImageField(upload_to="post_cover_img/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="liked_posts", blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )
    keywords = models.ManyToManyField(Keyword, related_name='posts', blank=True)

    def __str__(self):
        return self.title


# 댓글 테이블
class Comment(models.Model):
    content = models.CharField(max_length=100)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content