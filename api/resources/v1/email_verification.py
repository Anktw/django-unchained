from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
import os
from django.conf import settings
from django.db import transaction
from api import serializers
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import EmailMessage

class EmailVerificationCodeView(APIView):
    permission_classes = (AllowAny,)
    BASE_URL = os.path.join(settings.APP_DOMAIN, 'auth/signup/')

    @transaction.atomic
    def post(self, request):
        serializer = serializers.EmailVerificationCodeSerializer(data=request.data, user=request.user)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()

        self.send_verification_code(email=obj.email, verification_code=obj.verification_code)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def send_verification_code(self, email, verification_code):
        url=self.BASE_URL.rstrip('/') + f'/{verification_code}'
        subject = 'Please confirm your email address'
        body = (f'Thank you for signining up {settings.APP_NAME}.\n\n'
                f'Please take a second to finish your email verification '
                f'and sign up from the following URL.\n{url}\n\n'
                f'Note that the above verification link expires in '
                f'{settings.EMAIL_VERIFICATION_LIFETIME_MINS} minutes.\n'
                f'If this was a mistake, the account will not be created.')
        email = EmailMessage(subject=subject, body=body, to=[email])
        email.send()

class VerifiedEmailView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = serializers.VerifiedEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
