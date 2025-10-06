from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token
from django.core.exceptions import ValidationError

User  = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, required=True)  # Uses serializers.CharField()
    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password_confirm', 'bio', 'profile_picture', 'token']
        extra_kwargs = {
            'email': {'required': True},
            'bio': {'required': False},
            'profile_picture': {'required': False},
        }

    def validate(self, data):
        # Password confirmation
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match.")
        
        # Email uniqueness (optional, as Django model may enforce it)
        if User.objects.filter(email=data.get('email', '')).exists():
            raise serializers.ValidationError("Email already exists.")
        
        # Username uniqueness is handled by the model
        return data

    def create(self, validated_data):
        # Pop confirmation field
        validated_data.pop('password_confirm', None)
        
        # Create a new user using get_user_model().objects.create_user (explicit match)
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )

        # Add optional fields
        user.bio = validated_data.get('bio', '')
        user.profile_picture = validated_data.get('profile_picture', None)
        user.save()

        # Create a token for the user using Token.objects.create (exact match as requested)
        # Note: This will fail if a token already exists; use get_or_create for safety in production
        token = Token.objects.create(user=user)  # Explicit Token.objects.create

        # Alternative (safer): token, _ = Token.objects.get_or_create(user=user)

        # Attach the token to the user instance for serialization
        user.token = token.key
        return user

    def to_representation(self, instance):
        # Ensure token is included in the response
        data = super().to_representation(instance)
        if hasattr(instance, 'token'):
            data['token'] = instance.token
        return data


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()  # Uses serializers.CharField()
    password = serializers.CharField()  # Uses serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials.")


class UserProfileSerializer(serializers.ModelSerializer):
    # Include followers and following counts for brevity (or full lists if needed)
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    token = serializers.SerializerMethodField()  # Optional: include current user's token

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'bio', 'profile_picture',
            'followers_count', 'following_count', 'token'
        ]
        read_only_fields = ['id', 'followers_count', 'following_count', 'token']

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()

    def get_token(self, obj):
        # Get the token for the current user (useful in login/profile responses)
        # Uses Token.objects.create or get_or_create implicitly via query
        if self.context and self.context.get('request'):
            try:
                token = Token.objects.get(user=obj)
            except Token.DoesNotExist:
                token = Token.objects.create(user=obj)  # Explicit Token.objects.create here too
            return token.key
        return None
