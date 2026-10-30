import os

support_path = "support/services.py"
os.makedirs("support", exist_ok=True)

email_service_code = """
from django.core.mail import send_mail
from django.conf import settings

def send_enterprise_alert(user_email, subject, message):
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'admin@assetportfolio.com'),
            recipient_list=[user_email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Email dispatch error: {e}")
        return False
"""

if not os.path.exists(support_path):
    with open(support_path, "w", encoding="utf-8") as f:
        f.write(email_service_code)
    print("SUCCESS: Created support/services.py with enterprise email alert dispatch!")
else:
    with open(support_path, "r", encoding="utf-8") as f:
        content = f.read()
    if "send_enterprise_alert" not in content:
        with open(support_path, "a", encoding="utf-8") as f:
            f.write("\n" + email_service_code)
        print("SUCCESS: Added enterprise email alert dispatch service!")
    else:
        print("NOTICE: Email dispatch service already present.")
