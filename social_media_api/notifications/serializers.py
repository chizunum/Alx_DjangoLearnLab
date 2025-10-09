# notifications/serializers.py
from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.StringRelatedField()
    # Provide a simple repr for target
    target_repr = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ["id", "actor", "verb", "target_repr", "read", "timestamp"]

    def get_target_repr(self, obj):
        try:
            return str(obj.target)
        except Exception:
            return None
