import os

form_path = "documents/forms.py"
os.makedirs("documents", exist_ok=True)

form_code = """
from django import forms
from django.core.exceptions import ValidationError

class StrictDocumentUploadForm(forms.Form):
    title = forms.CharField(max_length=100)
    document_file = forms.FileField()

    def clean_document_file(self):
        uploaded_file = self.cleaned_data.get('document_file')
        
        if uploaded_file:
            # 1. Enforce strict file size limit (Max 5MB)
            max_size = 5 * 1024 * 1024  # 5MB in bytes
            if uploaded_file.size > max_size:
                raise ValidationError("File size exceeds the 5MB enterprise security limit[cite: 1].")
            
            # 2. Allow-list specific MIME types (PDF, JPEG, PNG)
            allowed_mimeTypes = ['application/pdf', 'image/jpeg', 'image/png']
            file_mime = getattr(uploaded_file, 'content_type', '')
            
            if file_mime not in allowed_mimeTypes:
                raise ValidationError(f"Invalid file type ({file_mime}). Only PDF, JPEG, and PNG files are permitted[cite: 1].")
                
        return uploaded_file
"""

with open(form_path, "w", encoding="utf-8") as f:
    f.write(form_code)

print("SUCCESS: Strict file size limits and MIME type allow-listing form created!")
