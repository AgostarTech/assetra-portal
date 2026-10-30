
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
