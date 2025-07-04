from django.db import models
from api.common import constants
from core.models.base_models import BaseTenantModel

class TenantAdminManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role_type = constants.TENANT_USER_ROLE_TYPE.ADMIN.value)
    

class TenantUser(BaseTenantModel):
    class Meta(BaseTenantModel.Meta):
        db_table = 'tenant_users'
        constraints = [models.UniqueConstraint(fields=['tenant_id', 'user_id'], name='unique_tenant_user'),]

    user = models.ForeignKey('User', unique=False, null=False, blank=False, on_delete=models.CASCADE)
    role_type = models.IntegerField(unique=False, null=False, blank=True, default=constants.TENANT_USER_ROLE_TYPE.GENERAL.value)
    joined_at = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    objects = models.Manager()
    tenant_admins = TenantAdminManager()
    @classmethod
    def get_id_from(cls, tenant_id, user_id):
        return cls.objects.get(tenant_id=tenant_id, user_id=user_id).id
    def __str__(self):
        return (f'({self.id}){self.tenant.name}, 'f'{self.user.email}')
            