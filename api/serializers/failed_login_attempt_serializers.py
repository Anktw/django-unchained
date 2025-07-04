from api.serializers.base_serializers import BaseModelSerializer
from rest_framework import serializers
from core import models


class FailedLoginAttemptSerializer(BaseModelSerializer):
    attempted_at = serializers.DateTimeField(required=False, read_only=True)
    """
    Serializer for FailedLoginAttempt model.
    Includes attempted_at as a read-only timestamp.
    """
    class Meta(BaseModelSerializer.Meta):
        model = models.FailedLoginAttempt