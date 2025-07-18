import pytest
from pytest_django.lazy_django import skip_if_no_django
from helpers.utils import *
from django.core.management import call_command
from django.db import connection
from rest_framework import status

import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'helpers'))


@pytest.fixture()
def client():
    skip_if_no_django()
    from helpers.client import CustomClient
    return CustomClient()

@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('reset_db', '--noinput')
        call_command('migrate')

@pytest.fixture()
def base_url():
    return os.path.join(os.environ['APP_DOMAIN'], '/api/v1')

@pytest.fixture(scope='class')
def reset_sequence(django_db_setup, django_db_blocker):
    def _reset_sequence(*args, **kwargs):
        model = args[0]
        with connection.cursor() as cursor:
            db_table = model._meta.db_table
            return cursor.execute(f'ALTER SEQUENCE {db_table}_id_seq RESTART WITH 1')
    return _reset_sequence

@pytest.fixture(scope='function')
def token(django_db_setup, client, base_url):
    def _token(*args, **kwargs):
        email = args[0]
        password = default_password() if len(args) == 1 else args[1]
        query = models.User.objects.filter(email=email)
        if query.count() == 0:
            raise RuntimeError(f'User(email) must be properly prepared before using client.')
        req = dict(data=dict(email=email, password=password))
        res = client.post(f'{base_url}/token/', req['data'])
        if res.status_code != status.HTTP_200_OK:
            raise RuntimeError(f'Failed to get token for user({email}).')
        if 'access' not in res.data:
            raise RuntimeError(f'Access token not found in response.')
        return res.data['access']
    return _token

@pytest.fixture(scope='function')
def bearer_token(token):
    def _bearer_token(*args, **kwargs):
        return f'Bearer {token(*args, **kwargs)}'
    return _bearer_token

@pytest.fixture(scope='function')
def email_verification_code(client, base_url):
    def _email_verification_code(*args, **kwargs):
        email = args[0]
        data = {'email': email, 'valid_till': get_verification_code_valid_till()}
        res = client.post(f'{base_url}/email/signup/verification/', data)
        if res.status_code != status.HTTP_200_OK:
            raise RuntimeError(f'get_verification_code({email}) failed. Status: {res.status_code}, Response: {res.json()}')
        return res.data['verification_code']
    return _email_verification_code

@pytest.fixture(scope='class')
def setup_users(django_db_blocker, reset_sequence):
    with django_db_blocker.unblock():
        model = models.User
        model.objects.all().delete()
        reset_sequence(model)
        call_command('insert_test_users')

@pytest.fixture(scope='class')
def setup_tenants(django_db_blocker, reset_sequence):
    with django_db_blocker.unblock():
        model = models.Tenant
        model.objects.all().delete()
        reset_sequence(model)
        call_command('insert_test_tenants')

@pytest.fixture(scope='class')
def setup_tenant_users(django_db_blocker, setup_users, setup_tenants, reset_sequence):
    with django_db_blocker.unblock():
        model = models.TenantUser
        model.objects.all().delete()
        reset_sequence(model)
        call_command('insert_test_tenant_users')
