from core.models.base_models import BaseModel
from django.db import models
from api.common import utils
from django.conf import settings
import datetime

class EmailVerification(BaseModel):
    class Meta(BaseModel.Meta):
        db_table = 'email_verification'
    
    email = models.EmailField(max_length=200, unique=False, null=False, blank=False)
    verification_code = models.CharField(max_length=200, unique=True, null=False, blank=False)
    valid_till = models.DateTimeField(unique=False, null=False, blank=False)


    def set_verification(self):
        self.verification_code = utils.generate_random_letters(length=settings.EMAIL_VERIFICATION_LENGTH)
        self.valid_till = utils.get_utc_now() + datetime.timedelta(minutes=settings.EMAIL_VERIFICATION_LIFETIME_MINS)
        
    def __str__(self):
        return (f'({self.id}){self.email}, 'f'{self.verification_code}')