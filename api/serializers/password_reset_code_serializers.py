from api.serializers.base_serializers import BaseModelSerializer, BaseSerializer
from core import models
from rest_framework.exceptions import ValidationError
from api.common import exceptions, utils
from rest_framework import serializers
from django.conf import settings



class PasswordResetCodeSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = models.PasswordReset
        read_only_fields = (('reset_code', 'valid_till',) + BaseModelSerializer.Meta.read_only_fields)

    def create(self, validated_data):
        user = models.User.objects.filter(email=validated_data['email']).first()
        if not user:
            raise exceptions.EmailNotRegistered(f'{validated_data["email"]} is not signed up.')

        # Remove user from validated_data since PasswordReset model doesn't have a user field
        password_reset_code = models.PasswordReset(**validated_data)
        password_reset_code.set_reset()
        password_reset_code.save()
        return password_reset_code
    
    def validate(self, data):
        if not models.User.objects.filter(email=data['email']).exists():
            raise exceptions.EmailNotRegistered(f'{data["email"]} is not signed up.')
        return data

class PasswordResetSerializer(BaseModelSerializer):
    reset_code = serializers.CharField()
    class Meta(BaseModelSerializer.Meta):
        model = models.User
        exclude = None
        fields = ('email', 'password', 'reset_code',)
        extra_kwargs = {**BaseModelSerializer.Meta.extra_kwargs,**{'password': { 'write_only': True },},}

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        instance.set_password(validated_data['password'])
        instance.save()
        return instance
    
    def validate(self, data):
        if not models.User.objects.filter(email=data['email']).exists():
            raise exceptions.EmailNotRegistered(f'{data["email"]} is not signed up.')

        query = models.PasswordReset.objects.filter(email=data['email'], reset_code=data['reset_code'])
        if query.count() == 0:
            raise ValidationError(f'Reset code for {data["email"]} is invalid.')

        password_reset_code = query.get()
        if utils.get_utc_now() > password_reset_code.valid_till:
            raise exceptions.PasswordResetCodeExpired()
        return data

class PasswordResetEmailSerializer(BaseSerializer):
    reset_code = serializers.CharField(max_length=settings.PASSWORD_RESET_LENGTH, write_only=True)
    email = serializers.CharField(max_length=200, required=False)

    def validate(self, data):
        if len(data['reset_code']) != settings.PASSWORD_RESET_CODE_LENGTH:
            raise serializers.ValidationError('Invalid password reset code.')

        query = models.PasswordReset.objects.filter(
        reset_code=data['reset_code'])
        if query.count() != 1:
            raise serializers.ValidationError('Invalid password reset code.')

        return query.get()
