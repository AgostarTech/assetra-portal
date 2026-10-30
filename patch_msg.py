import os

msg_path = "support/models.py"
os.makedirs("support", exist_ok=True)

model_addition = """
from django.conf import settings
from django.db import models

class ClientMessage(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=255)
    body = models.TextField()
    is_encrypted = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.recipient}: {self.subject}"
"""

with open(msg_path, "a", encoding="utf-8") as f:
    f.write("\n" + model_addition)

# Create a clean UI template for internal messaging
temp_path = "templates/support/internal_messaging.html"
os.makedirs("templates/support", exist_ok=True)

html_content = """{% extends "base.html" %}
{% block title %}Secure Internal Messaging - Asset Portal{% endblock %}
{% block page_title %}Secure Client-Manager Messaging{% endblock %}

{% block content %}
<div style="background: #fff; padding: 25px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
    <h3 style="margin-top: 0; color: #1a1a1a;">Encrypted Communication Roster</h3>
    <p style="color: #666; font-size: 14px; margin-bottom: 20px;">Send and review direct secure notes regarding compliance reviews and asset valuations[cite: 1].</p>

    <div style="border: 1px solid #eee; border-radius: 6px; padding: 15px; margin-bottom: 20px; background: #fdfbf7;">
        <h4 style="margin: 0 0 10px 0; font-size: 14px; color: #1a1a1a;">New Secure Message</h4>
        <form method="POST">
            {% csrf_token %}
            <div style="margin-bottom: 12px;">
                <input type="text" name="subject" placeholder="Subject / Reference (e.g., Compliance Document Feedback)" style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;" required>
            </div>
            <div style="margin-bottom: 12px;">
                <textarea name="body" rows="3" placeholder="Enter encrypted message contents..." style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;" required></textarea>
            </div>
            <button type="submit" style="background: #1a1a1a; color: #cfa76e; border: none; padding: 10px 18px; font-weight: bold; border-radius: 4px; cursor: pointer;">Send Encrypted Note</button>
        </form>
    </div>
</div>
{% endblock %}
"""

with open(temp_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("SUCCESS: Secure Internal Messaging model and template created!")
