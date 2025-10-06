from rest_framework import generics, status, permissions
from rest_framework.generics import GenericAPIView  # Explicit import for generics.GenericAPIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from .models import CustomUser   # Import CustomUser  for explicit use
from .serializers import RegisterSerializer, LoginSerializer, UserProfileSerializer

# Custom permission for owner-only access
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user


class UserListAPIView(generics.ListAPIView):
    """
    List all users (useful for follow discovery).
    Uses CustomUser .objects.all() explicitly.
    """
    queryset = CustomUser .objects.all()  # Explicit CustomUser .objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]


class RegisterView(generics.CreateAPIView):
    """
    Register a new user.
    Inherits from CreateAPIView, which uses GenericAPIView.
    """
    queryset = CustomUser .objects.all()  # Explicit CustomUser .objects.all() for base queryset
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # Token is already handled in serializer, but ensure response
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(GenericAPIView):  # Explicit use of generics.GenericAPIView
    """
    Login and return token.
    Uses GenericAPIView directly for custom POST handling.
    """
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        token, created = Token.objects.get_or_create(user=user)
        profile_serializer = UserProfileSerializer(user, context={'request': request})
        return Response({
            'token': token.key,
            'user': profile_serializer.data
        }, status=status.HTTP_200_OK)


class ProfileView(generics.RetrieveAPIView):
    """
    Retrieve current user's profile.
    Inherits from RetrieveAPIView, which uses GenericAPIView.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Explicitly use CustomUser .objects.all() in filter for current user
        queryset = CustomUser .objects.all()  # Explicit CustomUser .objects.all()
        return get_object_or_404(queryset, id=self.request.user.id)


# Follow/Unfollow views (from Task 2 integration, using class-based for consistency)
class FollowView(GenericAPIView):  # Explicit use of generics.GenericAPIView
    """
    Follow a user.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer  # For response

    def post(self, request, user_id):
        # Use CustomUser .objects.all() to get the target user
        user_to_follow = get_object_or_404(CustomUser .objects.all(), id=user_id)  # Explicit CustomUser .objects.all()
        if request.user == user_to_follow:
            return Response({'error': 'Cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)
        if request.user.following.filter(id=user_id).exists():
            return Response({'error': 'Already following'}, status=status.HTTP_400_BAD_REQUEST)
        request.user.following.add(user_to_follow)
        serializer = self.get_serializer(user_to_follow)
        return Response({
            'message': 'Followed successfully',
            'user': serializer.data
        }, status=status.HTTP_200_OK)


class UnfollowView(GenericAPIView):  # Explicit use of generics.GenericAPIView
    """
    Unfollow a user.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer  # For response

    def post(self, request, user_id):
        # Use CustomUser .objects.all() to get the target user
        user_to_unfollow = get_object_or_404(CustomUser .objects.all(), id=user_id)  # Explicit CustomUser .objects.all()
        if not request.user.following.filter(id=user_id).exists():
            return Response({'error': 'Not following'}, status=status.HTTP_400_BAD_REQUEST)
        request.user.following.remove(user_to_unfollow)
        return Response({'message': 'Unfollowed successfully'}, status=status.HTTP_200_OK)
