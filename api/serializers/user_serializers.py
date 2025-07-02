import logging
from api.serializers.base_serializers import BaseModelSerializer
from rest_framework import serializers
from core import models
from rest_framework.exceptions import ValidationError
from api.common import utils, exceptions

logger = logging.getLogger(__name__)


class NewUserSerializer(BaseModelSerializer):
    invitation_code = serializers.CharField(required=False, write_only=True)
    verification_code = serializers.CharField(required=False, write_only=True)

    class Meta(BaseModelSerializer.Meta):
        model = models.User
        read_only_fields = (('status',) + BaseModelSerializer.Meta.read_only_fields)
        extra_kwargs = {**BaseModelSerializer.Meta.extra_kwargs, **{'password': {'write_only': True},},}

    def create(self, validated_data):
        validated_data= self.creatorstamp(validated_data)
        if('invitation_code' not in validated_data) and ('verification_code' not in validated_data):
            raise ValidationError('Invitation code or verification code is needed to create')
        
        if 'invitation_code' in validated_data:
            validated_data.pop('invitation_code')
        if 'verification_code' in validated_data:
            validated_data.pop('verification_code')

        user = models.User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def validate(self, data):
        if 'invitation_code' in data:
            invitation_code = models.TenantInvitationCode.objects.get(email= data['email'], invitation_code = data['invitation_code'])
            if utils.get_utc_now() > invitation_code.valid_till:
                raise exceptions.EmailVerificationCodeExpired()
        data = self.set_blank_explicitly(data, fields=['groups', 'user_permissions'])

        return super().validate(data)
    

class UserSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = models.User
        read_only_fields = (('status',) + BaseModelSerializer.Meta.read_only_fields)
        exclude = ('password', ) + BaseModelSerializer.Meta.exclude

    def get_image(self):
        validate_data = self.creatorstamp(validate_data)
        user = models.User(**validate_data)
        user.set_password(validate_data['password'])
        user.save()
        return user
    
    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()
        return instance
    

class UserPasswordSerializer(BaseModelSerializer):
    password = serializers.CharField(max_length=200, min_length=8)
    new_password = serializers.CharField(required = False, max_length=200, min_length=8)

    class Meta:
        model = models.User
        exclude = None
        fields = ('password', 'new_password',)

    def update(self, instance, validated_data):
        validated_data['password'] = validated_data['new_password']
        validated_data.pop('new_password')

        instance = super().update(instance, validated_data)
        instance.set_password(validated_data['password'])
        instance.save()

        return instance
    
    def validate(self, data):
        user = models.User.objects.get(pk=self.user.id)
        
        if not user.check_password(data['password']):
            raise ValidationError('Current password')
        if data['password'] == data['new_password']:
            raise ValidationError('New password is the same as current password.')
        return data