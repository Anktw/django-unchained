from django.contrib import admin
from core import models
from core.admin import admins

admin.site.register(models.EmailVerification, admins.EmailVerificationCodeAdmin)
admin.site.register(models.PasswordReset, admins.PasswordResetCodeAdmin)
admin.site.register(models.User, admins.CustomUserAdmin)
admin.site.register(models.Tenant, admins.TenantAdmin)
admin.site.register(models.TenantInvitationCode, admins.TenantInvitationCodeAdmin)
admin.site.register(models.TenantUser, admins.TenantUserAdmin)
