import os
from api.common.utils import generate_random_letters
from core.models.base_models import BaseUserModel
from django.db import models

def get_user_image_path(instance, filename):
    _, ext = os.path.splittext(filename)
    filename = generate_random_letters(length=24) + ext
    return f"images/user/{instance.id}/{filename}"

class User(BaseUserModel):
    class Meta(BaseUserModel.Meta):
        db_table = 'users'
    disble_promotion = models.BooleanField(null=False, blank=False, default=False)
    email = models.EmailField(max_length=200, unique=True, null=False, blank=False)
    first_name = models.CharField(max_length=200, unique=False, null=False, blank=False)
    last_name = models.CharField(max_length=200, unique=False, null=False, blank=False)
    image = models.ImageField(verbose_name='user image', null=True, blank=True, upload_to=get_user_image_path)
    language_code = models.CharField(max_length=20, null=False, blank=False, default='en')
    status = models.IntegerField(unique=False, null=False, blank=False, default=0)
    timezone_code = models.CharField(max_length=200, null=False, blank=False, default='India/Kolakata')

    def __str__(self):
        return f'({self.id}){self.first_name},{self.last_name},{self.email}'
