import os
import sys
import django
from django.conf import settings

# Add the project path to sys.path
sys.path.insert(0, os.path.dirname(__file__))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
os.environ.setdefault('TEST', 'True')
django.setup()

from api.tests.helpers.client import CustomClient

client = CustomClient()
res = client.get('/api/v1/users/1/tenants/')
print(f"Status code: {res.status_code}")
print(f"Response content: {res.content}")
print(f"Response data: {getattr(res, 'data', 'No data attribute')}")
