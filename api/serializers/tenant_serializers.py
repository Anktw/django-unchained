from api.serializers.base_serializers import BaseModelSerializer
from rest_framework import serializers
from core import models
from api.common import utils
from django.conf import settings

class TenantSerializer(BaseModelSerializer):
    tenant_user_count = serializers.SerializerMethodField()

    class Meta(BaseModelSerializer.Meta):
        model = models.Tenant
        base_read_only_fields = BaseModelSerializer.Meta.read_only_fields
        if not isinstance(base_read_only_fields, (list, tuple)):
            base_read_only_fields = (base_read_only_fields,) if base_read_only_fields else ()
        
        read_only_fields = ('domain', ) + tuple(base_read_only_fields)

    def get_image(self, obj):
        request = self.context.get('request')
        image = models.User.image.url
        return request.build_absolute_url(image)

    def get_tenant_user_count(self, obj):
        try:
            count = models.TenantUser.objects.filter(tenant_id=obj.id).count()
        except:
            return 0
        
        return count
    
    def create(self, validated_data):
        validated_data['domain'] = utils.generate_random_letters(length=settings.TENANT_DOMAIN_LENGTH)
        
        return super().create(validated_data)