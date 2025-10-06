from django.urls import path
from .views import RegisterView, UserProfileView, follow_user, unfollow_user
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', obtain_auth_token),
    path('profile/<int:pk>/', UserProfileView.as_view()),
    path('follow/<int:user_id>/', follow_user),
    path('unfollow/<int:user_id>/', unfollow_user),
]
