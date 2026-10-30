import os

upload_path = "templates/documents/document_upload.html"
os.makedirs("templates/documents", exist_ok=True)

html_content = """{% extends "base.html" %}
{% block title %}Upload Document - Asset Portal{% endblock %}
{% block page_title %}Compliance Document Management{% endblock %}

{% block content %}
<div style="max-width: 600px; margin: 40px auto; background: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
    <h3 style="margin-top: 0; color: #1a1a1a;">Secure Document Upload</h3>
    <p style="color: #666; font-size: 14px;">Drag and drop your compliance files below or click to browse.</p>

    <form method="POST" enctype="multipart/form-data" id="upload-form">
        {% csrf_token %}
        <div id="drop-zone" style="border: 2px dashed #cfa76e; padding: 40px; text-align: center; border-radius: 6px; background: #fdfbf7; cursor: pointer; margin-bottom: 20px;">
            <span style="font-size: 32px; display: block; margin-bottom: 10px;">📁</span>
            <span style="font-weight: bold; color: #1a1a1a;">Drag & Drop files here, or click to select</span>
            <input type="file" name="document" id="file-input" style="display: none;" required>
        </div>
        <button type="submit" style="width: 100%; background: #1a1a1a; color: #cfa76e; border: none; padding: 12px; font-weight: bold; border-radius: 4px; cursor: pointer;">Upload Securely</button>
    </form>
</div>

<script>
    const dropZone = document.getElementById("drop-zone");
    const fileInput = document.getElementById("file-input");

    dropZone.addEventListener("click", () => fileInput.click());

    dropZone.addEventListener("dragover", (e) => {
        e.preventDefault();
        dropZone.style.background = "#f4f0e6";
    });

    dropZone.addEventListener("dragleave", () => {
        dropZone.style.background = "#fdfbf7";
    });

    dropZone.addEventListener("drop", (e) => {
        e.preventDefault();
        dropZone.style.background = "#fdfbf7";
        if (e.dataTransfer.files.length > 0) {
            fileInput.files = e.dataTransfer.files;
            dropZone.querySelector("span:nth-child(2)").innerText = "Selected: " + e.dataTransfer.files[0].name;
        }
    });

    fileInput.addEventListener("change", () => {
        if (fileInput.files.length > 0) {
            dropZone.querySelector("span:nth-child(2)").innerText = "Selected: " + fileInput.files[0].name;
        }
    });
</script>
{% endblock %}
"""

with open(upload_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("SUCCESS: Drag-and-drop document upload template created successfully!")
