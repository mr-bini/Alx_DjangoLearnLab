from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # User Authentication URLs
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),

    # Blog Post URLs (using singular 'post/' as per previous updates)
    path('post/', views.PostListView.as_view(), name='post_list'),  # List all posts
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),  # Detail view
    path('post/<int:pk>/update/', views.PostUpdateView.as_as_view(), name='post_update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),

    # Comment URLs (updated to match your exact patterns: singular 'comment/', 'update/', and <int:pk>)
    path('post/<int:pk>/comments/new/', views.CommentCreateView.as_view(), name='comment_create'),  # Matches "post/<int:pk>/comments/new/"
    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment_update'),  # Matches "comment/<int:pk>/update/"
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),  # Matches "comment/<int:pk>/delete/"

    # Tagging URLs
    path('tags/<slug:tag_slug>/', views.posts_by_tag, name='posts_by_tag'),

    # Search URL
    path('search/', views.search_posts, name='search_posts'),
]
