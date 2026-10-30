from django.contrib import admin
from django.utils import timezone
from django.contrib import messages
from .models import Document

# Define the custom action
@admin.action(description='Mark selected documents as APPROVED')
def bulk_approve_documents(modeladmin, request, queryset):
    updated = queryset.update(
        status='APPROVED',
        reviewed_by=request.user,
        reviewed_at=timezone.now()
    )
    modeladmin.message_user(
        request, 
        f'{updated} documents were successfully verified and approved.', 
        messages.SUCCESS
    )

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('category', 'uploader', 'asset', 'status', 'uploaded_at', 'reviewed_by')
    list_filter = ('status', 'category', 'uploaded_at')
    search_fields = ('uploader__username', 'asset__name')
    readonly_fields = ('uploaded_at', 'updated_at')
    
    # Register the custom action
    actions = [bulk_approve_documents]
    
    # Define fieldsets to logically group the document data vs the review workflow data
    fieldsets = (
        ('Document Information', {
            'fields': ('uploader', 'asset', 'category', 'file', 'uploaded_at')
        }),
        ('Verification Workflow', {
            'fields': ('status', 'reviewed_by', 'reviewed_at', 'review_notes')
        }),
    )

    def save_model(self, request, obj, form, change):
        # Automatically record reviewer and timestamp if status changes to Approved/Rejected
        if change and 'status' in form.changed_data:
            if obj.status in [Document.StatusChoices.APPROVED, Document.StatusChoices.REJECTED]:
                obj.reviewed_by = request.user
                obj.reviewed_at = timezone.now()
        super().save_model(request, obj, form, change)
        
    # Restrict who can use this panel (Functional override)
    def has_module_permission(self, request):
        # Only allow Managers and Admins to see this in the sidebar
        return request.user.is_authenticated and (request.user.role in ['ROLE_MANAGER', 'ROLE_ADMIN'] or request.user.is_superuser)

admin.site.register(Document, DocumentAdmin)