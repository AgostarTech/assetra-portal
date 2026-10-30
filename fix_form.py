import os

form_path = "documents/forms.py"
if os.path.exists(form_path):
    with open(form_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    if "DocumentForm =" not in content:
        content += "\n\n# Alias for compatibility with views\nDocumentForm = StrictDocumentUploadForm\n"
        with open(form_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("SUCCESS: Added DocumentForm alias to documents/forms.py!")
else:
    print("Creating documents/forms.py...")
    os.makedirs("documents", exist_ok=True)
    with open(form_path, "w", encoding="utf-8") as f:
        f.write("from django import forms\n\nclass DocumentForm(forms.Form):\n    title = forms.CharField(max_length=100)\n    document_file = forms.FileField()\n")
