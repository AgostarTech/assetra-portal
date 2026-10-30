import os

bulk_path = "templates/documents/document_verification_queue.html"
os.makedirs("templates/documents", exist_ok=True)

html_content = """{% extends "base.html" %}
{% block title %}Document Verification Queue - Asset Portal{% endblock %}
{% block page_title %}Compliance Document Verification Queue{% endblock %}

{% block content %}
<div style="background: #fff; padding: 25px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
        <div>
            <h3 style="margin: 0; color: #1a1a1a;">Pending Verification Queue</h3>
            <p style="color: #666; font-size: 14px; margin: 5px 0 0 0;">Review and perform bulk approvals for client-submitted compliance records.</p>
        </div>
        <div>
            <button onclick="bulkApproveSelected()" style="background: #1a1a1a; color: #cfa76e; border: none; padding: 10px 18px; font-weight: bold; border-radius: 4px; cursor: pointer;">Bulk Approve Selected</button>
        </div>
    </div>

    <table style="width: 100%; border-collapse: collapse; margin-top: 15px;">
        <thead>
            <tr style="background: #f4f6f9; text-align: left; font-size: 13px; color: #555;">
                <th style="padding: 10px; border-bottom: 2px solid #ddd; width: 40px;"><input type="checkbox" id="select-all" onclick="toggleSelectAll(this)"></th>
                <th style="padding: 10px; border-bottom: 2px solid #ddd;">Client Username</th>
                <th style="padding: 10px; border-bottom: 2px solid #ddd;">Document Type</th>
                <th style="padding: 10px; border-bottom: 2px solid #ddd;">Submission Date</th>
                <th style="padding: 10px; border-bottom: 2px solid #ddd;">Status</th>
            </tr>
        </thead>
        <tbody>
            <tr style="border-bottom: 1px solid #eee; font-size: 14px;">
                <td style="padding: 10px;"><input type="checkbox" class="doc-checkbox" value="1"></td>
                <td style="padding: 10px; font-weight: bold;">agola_waziri</td>
                <td style="padding: 10px;">Ownership Deed / Title</td>
                <td style="padding: 10px;">Oct 15, 2026</td>
                <td style="padding: 10px;"><span style="color: #856404; background: #fff3cd; padding: 3px 8px; border-radius: 4px; font-size: 12px; font-weight: bold;">Pending Review</span></td>
            </tr>
            <tr style="border-bottom: 1px solid #eee; font-size: 14px;">
                <td style="padding: 10px;"><input type="checkbox" class="doc-checkbox" value="2"></td>
                <td style="padding: 10px; font-weight: bold;">enterprise_client_beta</td>
                <td style="padding: 10px;">Audited Financial Statement</td>
                <td style="padding: 10px;">Oct 16, 2026</td>
                <td style="padding: 10px;"><span style="color: #856404; background: #fff3cd; padding: 3px 8px; border-radius: 4px; font-size: 12px; font-weight: bold;">Pending Review</span></td>
            </tr>
        </tbody>
    </table>
</div>

<script>
    function toggleSelectAll(source) {
        const checkboxes = document.querySelectorAll('.doc-checkbox');
        checkboxes.forEach(cb => cb.checked = source.checked);
    }

    function bulkApproveSelected() {
        const selected = document.querySelectorAll('.doc-checkbox:checked');
        if (selected.length === 0) {
            alert('Please select at least one document to approve.');
            return;
        }
        if (confirm('Are you sure you want to approve ' + selected.length + ' selected compliance document(s)?')) {
            alert('Successfully approved ' + selected.length + ' documents!');
            location.reload();
        }
    }
</script>
{% endblock %}
"""

with open(bulk_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("SUCCESS: Bulk-approval document queue template created successfully!")
