from django import forms
from django.core.exceptions import ValidationError
from .models import Document

class StrictDocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'category', 'asset', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g., Audited Statement 2026'}),
            'category': forms.Select(),
            'asset': forms.Select(),
            'file': forms.ClearableFileInput(attrs={'accept': '.pdf,.jpg,.jpeg,.png'}),
        }

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        # If user is provided, optionally filter assets belonging only to this user
        if self.user and hasattr(self.user, 'id'):
            from assets.models import Asset
            self.fields['asset'].queryset = Asset.objects.filter(owner=self.user, status=Asset.StatusChoices.ACTIVE)

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        
        if uploaded_file:
            # 1. Enforce strict file size limit (Max 5MB)
            max_size = 5 * 1024 * 1024  # 5MB in bytes
            if uploaded_file.size > max_size:
                raise ValidationError("File size exceeds the 5MB enterprise security limit.")
            
            # 2. Allow-list specific MIME types (PDF, JPEG, PNG)
            allowed_mimeTypes = ['application/pdf', 'image/jpeg', 'image/png']
            file_mime = getattr(uploaded_file, 'content_type', '')
            
            if file_mime not in allowed_mimeTypes:
                raise ValidationError(f"Invalid file type ({file_mime}). Only PDF, JPEG, and PNG files are permitted.")
                
        return uploaded_file

    def save(self, commit=True):
        document = super().save(commit=False)
        if self.user and not document.uploader_id:
            document.uploader = self.user
        if commit:
            document.save()
        return document

# Alias for compatibility with views
DocumentForm = StrictDocumentUploadForm