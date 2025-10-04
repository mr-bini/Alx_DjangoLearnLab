from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Post, Comment
from taggit.widgets import TagWidget  # Import for handling tags in forms


# ---------------------------
# User Registration Form
# ---------------------------

class CustomUser CreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Enter a valid email address.")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter email'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Enter password'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm password'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


# ---------------------------
# Blog Post Form (with TagWidget for tags)
# ---------------------------

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter post title',
                'class': 'form-control',
            }),
            'content': forms.Textarea(attrs={
                'placeholder': 'Enter post content',
                'rows': 10,
                'class': 'form-control',
            }),
            'tags': TagWidget(attrs={
                'placeholder': 'Enter tags (comma-separated, e.g., python,django)',
                'class': 'form-control',
            }),  # Uses TagWidget for comma-separated tag input
        }
        labels = {
            'title': 'Title',
            'content': 'Content',
            'tags': 'Tags',
        }
        help_texts = {
            'tags': 'Separate tags with commas (e.g., python, django, tutorial).',
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
                'class': 'form-control',
            }),
        }
        labels = {
            'content': 'Comment',
        }
