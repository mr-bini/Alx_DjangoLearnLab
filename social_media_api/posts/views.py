from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .models import Post, Like
from notifications.models import Notification
from .serializers import PostSerializer

User = get_user_model()


# 👇 Feed view (already fixed)
class FeedView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        following_users = user.following.all()
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)


# 👇 Like a post
class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)  # ✅ get_object_or_404
        like, created = Like.objects.get_or_create(user=request.user, post=post)  # ✅ Like.objects.get_or_create

        if created:
            # ✅ Notification for the post author
            if post.author != request.user:
                Notification.objects.create(
                    recipient=post.author,
                    actor=request.user,
                    verb="liked your post",
                    target=post
                )
            return Response({"message": "Post liked."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "You already liked this post."}, status=status.HTTP_200_OK)


# 👇 Unlike a post
class UnlikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        try:
            like = Like.objects.get(user=request.user, post=post)
            like.delete()
            return Response({"message": "Post unliked."}, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            return Response({"error": "You have not liked this post."}, status=status.HTTP_400_BAD_REQUEST)
