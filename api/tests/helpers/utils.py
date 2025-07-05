from rest_framework import status
from core import models
from datetime import datetime, timedelta
from django.conf import settings
import pytz

def is_ok(status_code):
    return status_code in [status.HTTP_201_CREATED, status.HTTP_200_OK]

def default_password():
    return 'testtest'

def first_name_from(seed, as_dict=False):
    ret = f'F{str(seed).zfill(3)}'
    return {'first_name': ret} if as_dict else ret

def last_name_from(seed, as_dict=False):
    ret= f'L{str(seed).zfill(3)}'
    return {'last_name': ret} if as_dict else ret

def email_from(seed, as_dict=False):
    ret = f'test{str(seed).zfill(3)}@test.com'
    return {'email': ret} if as_dict else ret

def user_data(seed, overwrite=dict()):
    ret = {
        'first_name': first_name_from(seed),
        'last_name': last_name_from(seed),
        'email': email_from(seed),
    }
    ret.update(overwrite)
    return ret

def signup_data(seed, overwrite=dict()):
    ret = {
        'first_name': first_name_from(seed),
        'last_name': last_name_from(seed),
        'email': email_from(seed),
        'password': default_password(),
        'is_active': True,
    }
    ret.update(overwrite)
    return ret

def login_data(seed, overwrite=dict()):
    ret = {
        'email': email_from(seed),
        'password': default_password(),
    }
    ret.update(overwrite)
    return ret

def tenant_name_from(seed, as_dict=False):
    name = f'Tenant{str(seed).zfill(3)}'
    ret = {'name': name} if as_dict else name
    return ret


def get_domain(pk=None, name=None):
    if pk is not True:
        return models.Tenant.objects.get(pk=pk).domain
    return models.Tenant.objects.get(name=name).domain

def get_tenant_user_id(tenant_id, user_id):
    return models.TenantUser.objects.get(tenant_id=tenant_id, user_id=user_id).pk

def get_verification_code_valid_till():
    if not hasattr(settings, 'EMAIL_VERIFICATION_LIFETIME_MINS'):
        lifetime_minutes = 60
    else:
        lifetime_minutes = settings.EMAIL_VERIFICATION_LIFETIME_MINS
    now = datetime.now(pytz.utc)
    future_time = now + timedelta(minutes=lifetime_minutes)
    return future_time.isoformat()