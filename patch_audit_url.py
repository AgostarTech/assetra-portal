import os

url_path = "audit/urls.py"
os.makedirs("audit", exist_ok=True)

url_content = """
from django.urls import path
from . import views

urlpatterns = [
    path('export/csv/', views.export_audit_logs_csv, name='export_audit_logs_csv'),
]
"""

if not os.path.exists(url_path):
    with open(url_path, "w", encoding="utf-8") as f:
        f.write(url_content)
    print("SUCCESS: Created audit/urls.py!")
else:
    with open(url_path, "r", encoding="utf-8") as f:
        content = f.read()
    if "export_audit_logs_csv" not in content:
        content = content.replace("urlpatterns = [", "urlpatterns = [\n    path('export/csv/', views.export_audit_logs_csv, name='export_audit_logs_csv'),")
        with open(url_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("SUCCESS: Added CSV export URL route!")
    else:
        print("NOTICE: Audit URL route already present.")

# Create a clean Admin Audit Dashboard template
dash_path = "templates/audit/audit_dashboard.html"
os.makedirs("templates/audit", exist_ok=True)

html_content = """{% extends "base.html" %}
{% block title %}Immutable Audit Logs - Asset Portal{% endblock %}
{% block page_title %}Enterprise Audit Trail & Regulatory Logs{% endblock %}

{% block content %}
<div style="background: #fff; padding: 25px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
        <div>
            <h3 style="margin: 0; color: #1a1a1a;">Immutable System Audit Trail</h3>
            <p style="color: #666; font-size: 14px; margin: 5px 0 0 0;">All requests, state changes, and user actions are securely recorded.</p>
        </div>
        <div>
            <a href="{% url 'export_audit_logs_csv' %}" style="background: #1a1a1a; color: #cfa76e; padding: 10px 18px; border-radius: 4px; font-weight: bold; text-decoration: none; display: inline-block;">Export Audit Trail (CSV)</a>
        </div>
    </div>

    <table style="width: 100%; border-collapse: collapse; margin-top: 15px;">
        <thead>
            <tr style="background: #f4f6f9; text-align: left; font-size: 13px; color: #555;">
                <th style="padding: 10px; border-bottom: 2px solid #ddd;">Timestamp</th>
                <th style="padding: 10px; border-bottom: 2px solid #ddd;">User</th>
                <th style="padding: 10px; border-bottom: 2px solid #ddd;">Action</th>
                <th style="padding: 10px; border-bottom: 2px solid #ddd;">IP Address</th>
                <th style="padding: 10px; border-bottom: 2px solid #ddd;">Endpoint</th>
            </tr>
        </thead>
        <tbody>
            <tr style="border-bottom: 1px solid #eee; font-size: 14px;">
                <td style="padding: 10px;">Oct 17, 2026 15:30:12</td>
                <td style="padding: 10px; font-weight: bold;">agola_waziri</td>
                <td style="padding: 10px;">UPDATE_ASSET_VALUATION</td>
                <td style="padding: 10px;">127.0.0.1</td>
                <td style="padding: 10px;">/assets/update/</td>
            </tr>
            <tr style="border-bottom: 1px solid #eee; font-size: 14px;">
                <td style="padding: 10px;">Oct 17, 2026 14:15:00</td>
                <td style="padding: 10px; font-weight: bold;">agola_waziri</td>
                <td style="padding: 10px;">DOWNLOAD_STATEMENT_PDF</td>
                <td style="padding: 10px;">127.0.0.1</td>
                <td style="padding: 10px;">/portfolios/statement/pdf/</td>
            </tr>
        </tbody>
    </table>
</div>
{% endblock %}
"""

with open(dash_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("SUCCESS: Audit dashboard template created with CSV export button!")
