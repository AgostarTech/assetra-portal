import os

ver_path = "documents/models.py"
if os.path.exists(ver_path):
    with open(ver_path, "r", encoding="utf-8") as f:
        content = f.read()

    version_model = """

class DocumentVersion(models.Model):
    document = models.ForeignKey('Document', on_delete=models.CASCADE, related_name='versions')
    version_number = models.PositiveIntegerField(default=1)
    file = models.FileField(upload_to='document_versions/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    rejection_reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.document.title} - v{self.version_number}"
"""

    if "DocumentVersion" not in content:
        with open(ver_path, "a", encoding="utf-8") as f:
            f.write("\n" + version_model)
        print("SUCCESS: DocumentVersion model added to documents/models.py[cite: 1]!")
    else:
        print("NOTICE: DocumentVersion model already exists.")
