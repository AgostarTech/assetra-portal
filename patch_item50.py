import os

email_path = "documents/notifications.py"
os.makedirs("documents", exist_ok=True)

notification_code = """
from django.core.mail import send_mail
from django.conf import settings

def send_document_status_alert(user_email, document_title, new_status):
    \"\"\"
    Sends secure email notifications when verification status changes 
    without exposing sensitive financial details in the email body[cite: 1].
    \"\"\"
    subject = f"Compliance Status Update: {document_title}"
    message = (
        f"Hello,\\n\\n"
        f"Your compliance document '{document_title}' has been reviewed.\\n"
        f"Current Verification Status: {new_status.upper()}\\n\\n"
        f"Please log in to your secure portal dashboard to review details.\\n"
        f"Asset Portfolio Tracking & Management System"
    )
    
    try:
        send_mail(
            subject,
            message,
            getattr(settings, 'DEFAULT_FROM_EMAIL', 'compliance@assetportal.com'),
            [user_email],
            fail_silently=False,
        )
        print(f"EMAIL SUCCESS: Secure status alert sent to {user_email}")
        return True
    except Exception as e:
        print(f"Email dispatch warning: {e}")
        return False
"""

with open(email_path, "w", encoding="utf-8") as f:
    f.write(notification_code)

print("SUCCESS: Automated Email Notification Engine created successfully!")
