import os

faq_path = "templates/support/knowledge_base.html"
os.makedirs("templates/support", exist_ok=True)

html_content = """{% extends "base.html" %}
{% block title %}Knowledge Base FAQ - Asset Portal{% endblock %}
{% block page_title %}Integrated Knowledge Base & FAQ{% endblock %}

{% block content %}
<div style="max-width: 800px; margin: 20px auto; background: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
    <h3 style="margin-top: 0; color: #1a1a1a;">Frequently Asked Questions</h3>
    <p style="color: #666; font-size: 14px; margin-bottom: 25px;">Browse our verified self-service documentation to quickly resolve asset management and compliance questions before submitting a support ticket[cite: 1].</p>

    <div style="display: flex; flex-direction: column; gap: 15px;">
        <div style="background: #fdfbf7; border: 1px solid #cfa76e; padding: 15px; border-radius: 6px;">
            <h4 style="margin: 0 0 5px 0; color: #1a1a1a; font-size: 15px;">How do I upload compliance identity documents?</h4>
            <p style="margin: 0; font-size: 13px; color: #666;">Navigate to the Documents module, use the drag-and-drop upload zone to select your PDF or PNG file, and submit it for compliance officer review.</p>
        </div>
        <div style="background: #fdfbf7; border: 1px solid #cfa76e; padding: 15px; border-radius: 6px;">
            <h4 style="margin: 0 0 5px 0; color: #1a1a1a; font-size: 15px;">How is my total portfolio net worth calculated?</h4>
            <p style="margin: 0; font-size: 13px; color: #666;">The platform aggregates all active asset valuations in real time and applies currency conversion standards to display your net worth instantly.</p>
        </div>
        <div style="background: #fdfbf7; border: 1px solid #cfa76e; padding: 15px; border-radius: 6px;">
            <h4 style="margin: 0 0 5px 0; color: #1a1a1a; font-size: 15px;">What should I do if my valuation is flagged as stale?</h4>
            <p style="margin: 0; font-size: 13px; color: #666;">Assets unvalued for over 12 months trigger compliance alerts. Update the asset valuation via the inline editing table or request an appraisal review.</p>
        </div>
    </div>
</div>
{% endblock %}
"""

with open(faq_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("SUCCESS: Integrated Knowledge Base FAQ template created successfully!")
