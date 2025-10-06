from rest_framework import generics, permissions, serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.StringRelatedField()
    class Meta:
        model = Notification
        fields = ['id', 'actor', 'verb', 'timestamp', 'unread']

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)
