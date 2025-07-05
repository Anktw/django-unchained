from django.test.client import Client
from rest_framework import status


class CustomClient(Client):
    def __init__(self, **defaults):
        super().__init__(**defaults)
        self.raise_request_exception = True
        self.expect_validation_error = False

    def set_expect_validation_error(self, expect=True):
        """Set whether the client should raise ValidationError for 400 responses"""
        self.expect_validation_error = expect
        return self

    def get(self, path, data=None, follow=False, secure=False, content_type='application/json', bearer_token='', check_auth_guard=False, **extra):
        if check_auth_guard:
            res = self._request(method='GET', path=path, data=data, follow=follow, secure=secure, content_type=content_type, bearer_token='', **extra)
            assert res.status_code == status.HTTP_401_UNAUTHORIZED
        return self._request(method='GET', path=path, data=data, follow=follow, secure=secure, content_type=content_type, bearer_token=bearer_token, **extra)

    def post(self, path, data=None, follow=False, secure=False, content_type='application/json', bearer_token='', check_auth_guard=False, **extra):
        if check_auth_guard:
            res = self._request(method='POST', path=path, data=data, follow=follow, secure=secure, content_type=content_type, bearer_token='', **extra)
            assert res.status_code == status.HTTP_401_UNAUTHORIZED
        return self._request(method='POST', path=path, data=data, follow=follow, secure=secure, content_type=content_type, bearer_token=bearer_token, **extra)

    def put(self, path, data='', follow=False, secure=False, content_type='application/json', bearer_token='', check_auth_guard=False, **extra):
        if check_auth_guard:
            res = self._request(method='PUT', path=path, data=data, follow=follow, secure=secure, content_type=content_type, bearer_token='', **extra)
            assert res.status_code == status.HTTP_401_UNAUTHORIZED
        res = self._request(method='PUT', path=path, data=data, follow=follow, secure=secure, content_type=content_type, bearer_token=bearer_token, **extra)
        return res

    def patch(self, path, data='', follow=False, secure=False, content_type='application/json', bearer_token='', check_auth_guard=False, **extra):
        if check_auth_guard:
            res = self._request(method='PATCH', path=path, data=data, follow=follow, secure=secure, content_type=content_type, bearer_token='', **extra)
            assert res.status_code == status.HTTP_401_UNAUTHORIZED
        res = self._request(method='PATCH', path=path, data=data, follow=follow, secure=secure, content_type=content_type, bearer_token=bearer_token, **extra)
        return res

    def delete(self, path, data='', follow=False, secure=False, content_type='application/json', bearer_token='', check_auth_guard=False, **extra):
        if check_auth_guard:
            res = self._request(method='DELETE', path=path, data=data, follow=follow, secure=secure, content_type=content_type, bearer_token='', **extra)
            assert res.status_code == status.HTTP_401_UNAUTHORIZED
        res = self._request(method='DELETE', path=path, data=data, follow=follow, secure=secure, content_type=content_type, bearer_token=bearer_token, **extra)
        return res

    def _request(self, method, path, data, follow, secure, content_type, bearer_token, **extra):
        args = dict(path=path, data=data, follow=follow, secure=secure, content_type=content_type)
        auth_header = {'HTTP_AUTHORIZATION': bearer_token} if bearer_token else {}
        res = None
        method = method.upper()
        if method == 'GET':
            args.pop('content_type')
            extra['CONTENT_TYPE'] = content_type
            res = super().get(**args, **auth_header, **extra)
        elif method == 'POST':
            res = super().post(**args, **auth_header, **extra)
        elif method == 'PUT':
            res = super().put(**args, **auth_header, **extra)
        elif method == 'PATCH':
            res = super().patch(**args, **auth_header, **extra)
        elif method == 'DELETE':
            res = super().delete(**args, **auth_header, **extra)
        else:
            raise ValueError(f'Unsupported method: {method}')

        # If the client is configured to raise exceptions and we get an error response
        if self.raise_request_exception and self.expect_validation_error and hasattr(res, 'status_code'):
            if res.status_code >= 400:
                # Try to parse the response and raise appropriate exception
                try:
                    response_data = res.json()
                    if res.status_code == 400 and 'ValidationError' in response_data.get('type', ''):
                        from rest_framework.exceptions import ValidationError
                        messages = response_data.get('messages', [])
                        if messages:
                            # Create ValidationError with the message from the response
                            raise ValidationError(messages[0])
                        raise ValidationError("Validation error")
                except (ValueError, KeyError):
                    # If we can't parse the response, just return it
                    pass

        return res
