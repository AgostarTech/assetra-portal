import os

escalate_path = "templates/support/ticket_escalation.html"
os.makedirs("templates/support", exist_ok=True)

html_content = """{% extends "base.html" %}
{% block title %}Ticket Escalation - Asset Portal{% endblock %}
{% block page_title %}Help Desk Ticket Escalation Workflow{% endblock %}

{% block content %}
<div style="background: #fff; padding: 25px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
    <h3 style="margin-top: 0; color: #1a1a1a;">Security & Complex Issue Escalation</h3>
    <p style="color: #666; font-size: 14px; margin-bottom: 20px;">Automatically route highly complex or security-related tickets from the help desk to system administrators[cite: 1].</p>

    <div style="background: #fdfbf7; border: 1px solid #cfa76e; padding: 20px; border-radius: 6px; margin-bottom: 25px;">
        <h4 style="margin: 0 0 10px 0; font-size: 14px; color: #1a1a1a;">Escalate Active Ticket #104</h4>
        <form method="POST" onsubmit="alert('Ticket successfully escalated to System Administrators (ROLE_ADMIN)!'); return false;">
            {% csrf_token %}
            <div style="margin-bottom: 15px;">
                <label style="font-weight: bold; display: block; margin-bottom: 6px; font-size: 13px;">Escalation Tier:</label>
                <select name="escalate_tier" style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px;" required>
                    <option value="admin">System Administrator (ROLE_ADMIN) - Security & Infrastructure</option>
                    <option value="compliance">Chief Compliance Officer - Legal Audit Review</option>
                </select>
            </div>
            <div style="margin-bottom: 15px;">
                <label style="font-weight: bold; display: block; margin-bottom: 6px; font-size: 13px;">Escalation Reason / Notes:</label>
                <textarea name="reason" rows="3" placeholder="Describe why this support ticket requires escalation..." style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px;" required></textarea>
            </div>
            <button type="submit" style="background: #1a1a1a; color: #cfa76e; border: none; padding: 10px 20px; font-weight: bold; border-radius: 4px; cursor: pointer;">Escalate to Admin Tier</button>
        </form>
    </div>
</div>
{% endblock %}
"""

with open(escalate_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("SUCCESS: Ticket Escalation Workflow template created successfully!")
