import logging
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.db import transaction
from api import serializers
from rest_framework.response import Response
from rest_framework import status
from core import models

logger = logging.getLogger(__name__)

class PasswordResetCodeView(APIView):
    permission_classes = (AllowAny,)

    @transaction.atomic
    def post(self, request):
        serializer = serializers.PasswordResetCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.delete_password_reset_codes(email=serializer.validated_data['email'])
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_password_reset_codes(self, email):
        user = models.User.objects.filter(email=email).first()
        if user:
            query = models.PasswordReset.objects.filter(user=user)
            query.delete()
