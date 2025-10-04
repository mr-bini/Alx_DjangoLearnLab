from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from taggit.forms import TagWidget

from .models import Post, Comment


class CustomUser CreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'tags': TagWidget(attrs={'class': 'tag-input'}),
        }
        labels = {
            'title': 'Post Title',
            'content': 'Content',
            'tags': 'Tags (comma separated)',
        }


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label='Comment',
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment here...'}),
        max_length=1000,
        help_text='Max length: 1000 characters.'
    )

    class Meta:
        model = Comment
        fields = ['content']

