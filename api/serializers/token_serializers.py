from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from core import models
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from api.common import exceptions, utils
from django.conf import settings
from api.serializers.failed_login_attempt_serializers import FailedLoginAttemptSerializer
import datetime



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = models.User.EMAIL_FIELD
    ip_address = serializers.CharField(write_only=True, required=False)
    
    @classmethod
    def get_token(cls, user):
        return super().get_token(user)
    
    def validate(self, data):
        login_is_locked = self.attempted_login_too_many_times(data)
        try:
            data_tokens = super().validate(data)
        except AuthenticationFailed as e:
            self.record_failed_login_attempt(data)
            if login_is_locked:
                raise exceptions.LoginAttemptLimitError
            else:
                raise AuthenticationFailed(e)
            
        if login_is_locked:
            raise exceptions.LoginAttemptLimitError
        
        access_expires_in = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()
        refresh_expires_in = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()
        data['access_expires_in'] = int(access_expires_in)
        data['refresh_expires_in'] = int(refresh_expires_in)

        return data_tokens
    
    def record_failed_login_attempt(self, data):
        serializer = FailedLoginAttemptSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
    def attempted_login_too_many_times(self, data):
        date_to = utils.get_utc_now()
        date_from = date_to - datetime.timedelta(minutes=settings.LOGIN_LOCK_PERIOD_MINS)
        query = models.FailedLoginAttempt.objects.filter(email=data['email'], attempted_at__range=[date_from, date_to])
        if data['ip_address'] is not None:
            query = query.filter(ip_address=data['ip_address'])
            
        return query.count() >= settings.FAILED_LOGIN_ATTEMPT_MAX_COUNT
        
        
class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    @classmethod
    def get_token(cls, user):
        return super().get_token(user)
    
    def validate(self, data):
        data = super().validate(data)
        access_expires_in = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()
        data['access_expires_in'] = int(access_expires_in)
        
        return data