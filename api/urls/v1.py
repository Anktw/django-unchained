from django.urls import path



app_name = 'api'

tenant_url = 'tenants/<str:domain>/'
tenant_user_url