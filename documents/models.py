from django.db import models
from django.conf import settings
from assets.models import Asset

class Document(models.Model):
    class StatusChoices(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        SUBMITTED = 'SUBMITTED', 'Submitted'
        UNDER_REVIEW = 'UNDER_REVIEW', 'Under Review'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'

    class CategoryChoices(models.TextChoices):
        IDENTITY = 'IDENTITY', 'Identity Proof'
        OWNERSHIP = 'OWNERSHIP', 'Ownership Certificate'
        VALUATION = 'VALUATION', 'Valuation Report'
        OTHER = 'OTHER', 'Other'

    title = models.CharField(max_length=255, blank=True, help_text="Optional custom title for the document.")
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='uploaded_documents')
    asset = models.ForeignKey(Asset, on_delete=models.SET_NULL, null=True, blank=True, related_name='documents', help_text="Optional: Associate with a specific asset")
    
    category = models.CharField(max_length=50, choices=CategoryChoices.choices)
    # Files are stored in year/month directories. In production, this should be restricted storage.
    file = models.FileField(upload_to='secure_documents/%Y/%m/')
    
    status = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.DRAFT)
    
    # Verification Workflow Fields
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_documents')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    review_notes = models.TextField(blank=True, null=True, help_text="Reason for rejection or general review notes.")
    
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        doc_name = self.title or self.get_category_display()
        return f"{doc_name} - {self.uploader.username} ({self.get_status_display()})"


class DocumentVersion(models.Model):
    document = models.ForeignKey('Document', on_delete=models.CASCADE, related_name='versions')
    version_number = models.PositiveIntegerField(default=1)
    file = models.FileField(upload_to='document_versions/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    rejection_reason = models.TextField(blank=True, null=True)

    def __str__(self):
        doc_name = self.document.title or self.document.get_category_display()
        return f"{doc_name} v{self.version_number}"