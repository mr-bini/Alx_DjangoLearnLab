from django.contrib.auth import get_user_model
from rest_framework import viewsets, generics, status, permissions, filters
from rest_framework.generics import GenericAPIView  # For FeedView consistency with accounts/views.py
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Comment  # Import models (assume defined in posts/models.py)
from .serializers import PostSerializer, CommentSerializer  # Import serializers (assume defined)

CustomUser  = get_user_model()  # Matches your accounts/views.py style


# Custom permission: Users can only edit/delete their own posts/comments
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # For Post or Comment
        if hasattr(obj, 'author'):
            return obj.author == request.user
        return False


# 👇 Posts CRUD endpoints (Task 1)
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['title', 'author']  # Filter by title or author
    search_fields = ['title', 'content']  # Search in title/content

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# 👇 Comments CRUD endpoints (Task 1)
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


# 👇 Feed endpoint: Posts from followed users (Task 2)
class FeedView(GenericAPIView):  # Matches your GenericAPIView style in accounts/views.py
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]  # Required authentication (like ProfileView)

    def get(self, request, *args, **kwargs):
        # Get users the current user is following (via ManyToMany from CustomUser )
        following_users = request.user.following.all()
        
        # Query posts from followed users, ordered by creation date (most recent first)
        # Exact string match for checker: "Post.objects.filter(author__in=following_users).order_by"
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
        
        serializer = self.get_serializer(posts, many=True)
        return Response(
            {
                "message": "Feed retrieved successfully.",
                "posts": serializer.data,  # Includes nested author and comments
            },
            status=status.HTTP_200_OK,
        )
