from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Notification
from .serializers import NotificationSerializer

# Create your views here.


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None  # or use PageNumberPagination if needed

    def get_queryset(self):
        user = self.request.user
        # Optionally prioritize unread first
        return Notification.objects.filter(recipient=user).order_by("read", "-timestamp")


class MarkNotificationReadView(generics.UpdateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = "pk"

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        # allow partial update to mark read/unread
        return super().partial_update(request, *args, **kwargs)
