from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Asset, AssetDocument, AuditLog

@receiver(post_delete, sender=Asset)
def log_asset_deletion(sender, instance, **kwargs):
    """Log when an entire asset record is deleted."""
    AuditLog.objects.create(
        user=getattr(instance, '_deleted_by', None),
        action=AuditLog.ActionChoices.DELETE,
        model_name="Asset",
        object_id=instance.id,
        description=f"Deleted asset '{instance.name}' ({instance.get_category_display()}) with estimated value {instance.current_estimated_value} {instance.currency}."
    )

@receiver(post_delete, sender=AssetDocument)
def log_document_deletion(sender, instance, **kwargs):
    """Log when a specific supporting document/PDF is deleted."""
    asset_name = instance.asset.name if instance.asset else "Unlinked Asset"
    AuditLog.objects.create(
        user=getattr(instance, '_deleted_by', None),
        action=AuditLog.ActionChoices.DELETE,
        model_name="AssetDocument",
        object_id=instance.id,
        description=f"Deleted document '{instance.title}' ({instance.get_document_type_display()}) linked to asset '{asset_name}'."
    )