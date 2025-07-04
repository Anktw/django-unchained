from django.contrib import admin

class TenantUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'tenant_id', 'user_id', 'role_type',)
    list_display_links = list_display
    exclude = ('deleted_at',)
    search_fields = ('id', 'name',)
    ordering = ('id', 'tenant_id', 'user_id',)