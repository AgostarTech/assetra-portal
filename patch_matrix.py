import os

matrix_path = "templates/dashboards/manager_client_matrix.html"
os.makedirs("templates/dashboards", exist_ok=True)

html_content = """{% extends "base.html" %}
{% block title %}Client Overview Matrix - Asset Portal{% endblock %}
{% block page_title %}Wealth Advisor Client Portfolio Matrix{% endblock %}

{% block content %}
<div style="background: #fff; padding: 25px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
    <h3 style="margin-top: 0; color: #1a1a1a;">Assigned Client Portfolio Overview</h3>
    <p style="color: #666; font-size: 14px; margin-bottom: 20px;">Monitor aggregate health, Assets Under Management (AUM), and KYC compliance status for your assigned roster[cite: 1].</p>

    <table style="width: 100%; border-collapse: collapse; margin-top: 15px;">
        <thead>
            <tr style="background: #f4f6f9; text-align: left; font-size: 13px; color: #555;">
                <th style="padding: 10px; border-bottom: 2px solid #ddd;">Client Name</th>
                <th style="padding: 10px; border-bottom: 2px solid #ddd;">Total AUM</th>
                <th style="padding: 10px; border-bottom: 2px solid #ddd;">Portfolio Health</th>
                <th style="padding: 10px; border-bottom: 2px solid #ddd;">Compliance Status</th>
                <th style="padding: 10px; border-bottom: 2px solid #ddd;">Actions</th>
            </tr>
        </thead>
        <tbody>
            <tr style="border-bottom: 1px solid #eee; font-size: 14px;">
                <td style="padding: 10px; font-weight: bold;">Agola Waziri</td>
                <td style="padding: 10px;">$4,250,000.00</td>
                <td style="padding: 10px;"><span style="color: #155724; background: #d4edda; padding: 3px 8px; border-radius: 4px; font-size: 12px; font-weight: bold;">Optimal</span></td>
                <td style="padding: 10px;"><span style="color: #155724; background: #d4edda; padding: 3px 8px; border-radius: 4px; font-size: 12px; font-weight: bold;">Verified</span></td>
                <td style="padding: 10px;">
                    <a href="#" style="color: #cfa76e; text-decoration: none; font-weight: bold; font-size: 13px;">View Details</a>
                </td>
            </tr>
            <tr style="border-bottom: 1px solid #eee; font-size: 14px;">
                <td style="padding: 10px; font-weight: bold;">Enterprise Client Beta</td>
                <td style="padding: 10px;">$12,800,000.00</td>
                <td style="padding: 10px;"><span style="color: #856404; background: #fff3cd; padding: 3px 8px; border-radius: 4px; font-size: 12px; font-weight: bold;">Stable</span></td>
                <td style="padding: 10px;"><span style="color: #721c24; background: #f8d7da; padding: 3px 8px; border-radius: 4px; font-size: 12px; font-weight: bold;">Pending Review</span></td>
                <td style="padding: 10px;">
                    <a href="#" style="color: #cfa76e; text-decoration: none; font-weight: bold; font-size: 13px;">View Details</a>
                </td>
            </tr>
        </tbody>
    </table>
</div>
{% endblock %}
"""

with open(matrix_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("SUCCESS: Client Overview matrix template created successfully!")
