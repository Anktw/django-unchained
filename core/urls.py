from django.urls import path, re_path
from core.views import index

app_name = 'core'

urlpatterns = [path('', index),]

urlpatterns += [re_path('^.*$', index)]