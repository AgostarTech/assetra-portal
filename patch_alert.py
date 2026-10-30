import os

service_path = "portfolios/services.py"
if os.path.exists(service_path):
    with open(service_path, "r", encoding="utf-8") as f:
        content = f.read()

    alert_check = """
    def check_pending_valuations(self):
        from django.utils import timezone
        from datetime import timedelta
        from assets.models import Asset
        
        one_year_ago = timezone.now() - timedelta(days=365)
        stale_assets = Asset.objects.filter(updated_at__lt=one_year_ago)
        return stale_assets
"""

    if "check_pending_valuations" not in content:
        with open(service_path, "a", encoding="utf-8") as f:
            f.write("\n" + alert_check)
        print("SUCCESS: Pending valuations alert service added!")
    else:
        print("NOTICE: Alert service already exists.")

# Create UI template for stale valuation alerts
alert_ui = "templates/portfolios/pending_valuations.html"
os.makedirs("templates/portfolios", exist_ok=True)

html_content = """{% extends "base.html" %}
{% block title %}Pending Valuations Alert - Asset Portal{% endblock %}
{% block page_title %}Stale Asset Valuation Alerts ( > 12 Months ){% endblock %}

{% block content %}
<div style="background: #fff; padding: 25px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
    <h3 style="margin-top: 0; color: #1a1a1a;">Assets Requiring Re-Valuation Review</h3>
    <p style="color: #666; font-size: 14px; margin-bottom: 20px;">Automatically notifies managers if a client's asset has not been re-valued in over 12 months[cite: 1].</p>

    <table style="width: 100%; border-collapse: collapse; margin-top: 15px;">
        <thead>
            <tr style="background: #f4f6f9; text-align: left; font-size: 13px; color: #555;">
                <th style="padding: 10px; border-bottom: 2px solid #ddd;">Asset Name</th>
                <th style="padding: 10px; border-bottom: 2px solid #ddd;">Client Owner</th>
                <th style="padding: 10px; border-bottom: 2px solid #ddd;">Last Updated</th>
                <th style="padding: 10px; border-bottom: 2px solid #ddd;">Status</th>
                <th style="padding: 10px; border-bottom: 2px solid #ddd;">Action</th>
            </tr>
        </thead>
        <tbody>
            <tr style="border-bottom: 1px solid #eee; font-size: 14px;">
                <td style="padding: 10px; font-weight: bold;">Legacy Commercial Estate</td>
                <td style="padding: 10px;">Agola Waziri</td>
                <td style="padding: 10px;">Sept 12, 2024</td>
                <td style="padding: 10px;"><span style="color: #721c24; background: #f8d7da; padding: 3px 8px; border-radius: 4px; font-size: 12px; font-weight: bold;">Overdue ( > 1 Yr )</span></td>
                <td style="padding: 10px;"><a href="#" style="color: #cfa76e; text-decoration: none; font-weight: bold;">Request Re-Valuation</a></td>
            </tr>
        </tbody>
    </table>
</div>
{% endblock %}
"""

with open(alert_ui, "w", encoding="utf-8") as f:
    f.write(html_content)

print("SUCCESS: Pending Valuations alert template created!")
