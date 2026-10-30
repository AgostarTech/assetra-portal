from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("timestamp", "user", "action", "ip_address", "path")
    list_filter = ("action", "timestamp", "ip_address")
    search_fields = ("user__username", "path", "details", "ip_address")
    readonly_fields = ("user", "action", "path", "ip_address", "details", "timestamp")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

