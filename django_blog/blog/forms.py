from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Post, Comment
from taggit.widgets import TagWidget  # Explicit import for TagWidget


# ---------------------------
# User Registration Form
# ---------------------------

class CustomUser CreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Enter a valid email address.")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Enter username',
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter email',
                'class': 'form-control'
            }),
            'password1': forms.PasswordInput(attrs={
                'placeholder': 'Enter password',
                'class': 'form-control'
            }),
            'password2': forms.PasswordInput(attrs={
                'placeholder': 'Confirm password',
                'class': 'form-control'
            }),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


# ---------------------------
# Blog Post Form (Includes TagWidget for tags field)
# ---------------------------

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']  # Includes 'tags' field
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter post title',
                'class': 'form-control'
            }),
            'content': forms.Textarea(attrs={
                'placeholder': 'Enter post content',
                'rows': 10,
                'class': 'form-control'
            }),
            'tags': TagWidget(attrs={
                'placeholder': 'Enter tags (comma-separated, e.g., python,django)',
                'class': 'form-control'
            }),  # TagWidget() explicitly used here for comma-separated tag input
        }
        labels = {
            'title': 'Title',
            'content': 'Content',
            'tags': 'Tags',
        }
        help_texts = {
            'tags': 'Separate tags with commas (e.g., python, django, tutorial). Existing tags will be suggested.',
        }


# ---------------------------
# Comment Form
# ---------------------------

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Enter your comment...',
                'rows': 4,
                'class': 'form-control'
            }),
        }
        labels = {
            'content': 'Comment',
        }
