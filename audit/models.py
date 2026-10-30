from django.db import models
from django.conf import settings

class AuditLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="audit_logs")
    action = models.CharField(max_length=100)
    path = models.CharField(max_length=255, blank=True, null=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    details = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "Audit Log"
        verbose_name_plural = "Audit Logs"

    def __str__(self):
        username = self.user.username if self.user else "Anonymous"
        return f"[{self.timestamp}] {username} - {self.action} ({self.ip_address})"

    fn_locked = False

    def save(self, *args, **kwargs):
        if self.pk and not self.fn_locked:
            raise Exception("Audit logs are strictly immutable and cannot be modified.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise Exception("Audit logs are strictly immutable and cannot be deleted.")

