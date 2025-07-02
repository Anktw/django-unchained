import logging
from rest_framework import serializers
from django.conf import settings
from api.common import exceptions
from api.serializers.base_serializers import BaseModelSerializer
from api.serializers.tenant_serializers import TenantSerializer
from api.serializers.tenant_user_serializers import TenantUserSerializer
from core import models



logger = logging.getLogger(__name__)

class TenantInvitationCodeListSerializer(serializers.ListSerializer):
    def validate(self, data):
        if len(data) > settings.TENANT_INVITATION_CODE_MAX_SIZE:
            raise exceptions.RequestSizeError('List size must be <= 'f'{settings.TENANT_INVITATION_CODE_REQUEST_MAX_SIZE}.')
        
        if len(set([d['tenant_id'] for d in data])) > 1:
            raise serializers.ValidationError('Multiple tenant ids are contained.')

        if len(set([d['tenant_user_id'] for d in data])) > 1:
            raise serializers.ValidationError('Multiple tenant user ids are contained.')
        if len(set([d['email'] for d in data])) != len(data):
            raise serializers.ValidationError('Duplicated emails are in request.')  
        
        return data
    
class TenantInvitionCodeSerializer(BaseModelSerializer):
    tenant = TenantSerializer(required=False, read_only=True)
    tenant_user = TenantUserSerializer(required=False, read_only=True)
    invited_at = serializers.DateTimeField(required=False, read_only=True)
    tenant_id = serializers.IntegerField(write_only=True)
    tenant_user_id = serializers.IntegerField(write_only=True)

    class Meta(BaseModelSerializer.Meta):
        list_serializer_class=TenantInvitationCodeListSerializer
        model = models.TenantIn