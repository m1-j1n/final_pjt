from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    reading_date = forms.DateField(
        label='독서일',
        required=True,
        widget=forms.DateInput(attrs={
            'type': 'date'
        })
    )
    class Meta:
        model = Post
        exclude = ["cover_img", "likes", "user", "book", "created_at", "updated_at"]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('user', 'post', "created_at", "updated_at")