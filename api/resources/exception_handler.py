import logging
from django.http import Http404
from rest_framework import status
import django.core.exceptions as django_exceptions
import rest_framework as drf
from api.common import exceptions
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.settings import api_settings

logger = logging.getLogger(__name__)

exc2status_map = (
    {
        'type': Http404,
        'status': status.HTTP_404_NOT_FOUND
    },
    {
        'type': django_exceptions.PermissionDenied,
        'status': status.HTTP_403_FORBIDDEN,
    },
    {
        'type': drf.exceptions.NotFound,
        'status': status.HTTP_404_NOT_FOUND,
    },
    {
        'type': drf.exceptions.PermissionDenied,
        'status': status.HTTP_403_FORBIDDEN,
    },
    {
        'type': drf.exceptions.ValidationError,
        'status': status.HTTP_400_BAD_REQUEST,
    },
    {
        'type': drf.exceptions.NotAuthenticated,
        'status': status.HTTP_401_UNAUTHORIZED,
    },
    {
        'type': exceptions.DataAlreadyRegistered,
        'status': status.HTTP_409_CONFLICT,
    },
    {
        'type': exceptions.EmailNotRegistered,
        'status': status.HTTP_400_BAD_REQUEST,
    },
    {
        'type': exceptions.EmailVerificationCodeExpired,
        'status': status.HTTP_403_FORBIDDEN,
    },
    {
        'type': exceptions.OwnershipError,
        'status': status.HTTP_403_FORBIDDEN,
    },
    {
        'type': exceptions.PasswordResetCodeExpired,
        'status': status.HTTP_403_FORBIDDEN,
    },
    {
        'type': exceptions.RequestSizeError,
        'status': status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
    },
    {
        'type': exceptions.TenantInvitationCodeExpired,
        'status': status.HTTP_403_FORBIDDEN,
    },
)

def get_status_code(exc):
    for exc2status in exc2status_map:
        if isinstance(exc, exc2status['type']):
            return exc2status['status']
    return status.HTTP_500_INTERNAL_SERVER_ERROR

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    msg = {'exc': {exc}, 'view': context['view'] if 'view' in context else None, }
    logger.error(f'{type(exc)}: {exc}')
    get_status_code(exc)
    data = {
        'type': str(type(exc)),
        'action': str(context['view']),
        'messages': [str(exc)],
        'status': get_status_code(exc),
        'error': True,
    }
    if (response is None) or (not isinstance(response, Response)):
        response = Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        logger.error(f'Response data: {response.data}')
        return response
    
    if isinstance(exc.detail, dict):
        if isinstance(exc, drf.exceptions.ValidationError):
            messages = []
            for key, value in exc.detail.items():
                if key == api_settings.NON_FIELD_ERRORS_KEY:
                    messages.append(' '.join(value))
                else:
                    messages.append(f'{key}: {" ".join(value)}')
                data['messages'] = messages
        elif isinstance(exc.detail, list):
            data['messages'] = exc.detail
        else:
            data['messages'] = [exc.detail]
        logger.error(f'Response data: {response.data}')
        return Response(data, status=data['status'])