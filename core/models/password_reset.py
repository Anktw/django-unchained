from core.models.base_models import BaseModel
from django.db import models
from api.common import utils
from django.conf import settings
import datetime

class PasswordReset(BaseModel):
    class Meta(BaseModel.Meta):
        db_table = 'password_reset'
    
    email = models.EmailField(max_length=200, unique=False, null=False, blank=False)
    reset_code= models.CharField(max_length=200, unique=True, null=False, blank=False)
    valid_till = models.DateTimeField(unique=False, null=False, blank=False)


    def set_reset(self):
        self.reset_code = utils.generate_random_letters(length=settings.PASSWORD_RESET_LENGTH)
        self.valid_till = utils.get_utc_now() + datetime.timedelta(minutes=settings.PASSWORD_RESET_LIFETIME_MINS)

    def __str__(self):
        return (f'({self.id}){self.email},'f'{self.reset_code}')