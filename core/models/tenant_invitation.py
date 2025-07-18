from core.models.base_models import BaseTenantModel
from django.db import models
from api.common import utils
from django.conf import settings
import datetime

class TenantInvitation(BaseTenantModel):
    class Meta(BaseTenantModel.Meta):
        db_table = 'tenant_invitation'
    
    tenant_user = models.ForeignKey('TenantUser', unique=False, null=False, blank=False, on_delete=models.CASCADE)
    email = models.EmailField(max_length=200, unique=False, null=False, blank=False)
    invitation_code = models.CharField(max_length=200, unique=True, null=False, blank=False)
    invited_at = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    valid_till = models.DateTimeField(unique=False, null=False, blank=False)

    def set_invitation(self):
        self.invitation_code = utils.generate_random_letters(length=settings.TENANT_INVITATION_CODE_LENGTH)
        self.valid_till = utils.get_utc_now() + datetime.timedelta(minutes=settings.TENANT_INVITATION_CODE_LIFETIME_MINS)

    def __str__(self):
        return (f'({self.id}){self.tenant.name}, ' f'{self.tenant_user}, 'f'{self.email}, 'f'{self.invitation_code[:10]}')
        