from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # User Authentication URLs
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),

    # Blog Post URLs (using singular 'post/' as per your expectation)
    path('post/', views.PostListView.as_view(), name='post_list'),  # List all posts
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),  # Matches your "post/new/"
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),  # Detail view
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post_update'),  # Matches your "post/<int:pk>/update/"
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),  # Matches your "post/<int:pk>/delete/"

    # Comment URLs
    path('post/<int:post_id>/comments/new/', views.add_comment, name='add_comment'),
    path('comments/<int:pk>/edit/', views.CommentUpdateView.as_view(), name='comment_edit'),
    path('comments/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),

    # Tagging URLs
    path('tags/<slug:tag_slug>/', views.posts_by_tag, name='posts_by_tag'),

    # Search URL
    path('search/', views.search_posts, name='search_posts'),
]
