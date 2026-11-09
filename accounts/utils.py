import urllib.parse
import urllib.request
import json
from django.core.mail import send_mail
from django.conf import settings

def send_otp_notifications(user, telemetry=None):
    """
    Dispatches the unified 6-character alphanumeric OTP to both the user's
    registered email and mobile phone number, including full device/location telemetry.
    """
    if telemetry is None:
        telemetry = {}

    otp = user.otp_code
    if not otp:
        return

    # Extract telemetry details with safe fallbacks
    ip_address = telemetry.get('ip_address', 'Unknown')
    latitude = telemetry.get('latitude', 'Unknown')
    longitude = telemetry.get('longitude', 'Unknown')
    user_agent = telemetry.get('user_agent', 'Unknown Browser')
    screen_width = telemetry.get('screen_width', 'Unknown')
    device_name = telemetry.get('device_name', 'Standard Workstation')
    serial_number = telemetry.get('serial_number', 'N/A')

    # ==========================================
    # 1. EMAIL DISPATCH (Institutional Security Alert)
    # ==========================================
    if user.email:
        subject = "🔒 Security Alert: Assetra Portal Sign-In Verification"
        email_message = (
            f"Dear {user.first_name or 'Valued User'},\n\n"
            f"A login attempt was initiated for your Assetra account. To complete authentication, "
            f"please use the mandatory 6-character verification code below:\n\n"
            f"👉 VERIFICATION CODE: {otp}\n\n"
            f"----------------------------------------\n"
            f"SIGN-IN DEVICE & LOCATION AUDIT:\n"
            f"• IP Address: {ip_address}\n"
            f"• Approximate Location (Lat, Lon): {latitude}, {longitude}\n"
            f"• Browser / User-Agent: {user_agent}\n"
            f"• Screen Resolution Width: {screen_width}px\n"
            f"• Device / Company ID: {device_name}\n"
            f"• Hardware Serial Number: {serial_number}\n"
            f"----------------------------------------\n\n"
            f"If you did not initiate this request, please contact your system administrator immediately."
        )

        try:
            send_mail(
                subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            print(f"[Email Notification Sent]: Dispatched to {user.email}")
        except Exception as e:
            print(f"[Email OTP Error] Failed to send email to {user.email}: {e}")

    # ==========================================
    # 2. SMS DISPATCH (Native HTTP Gateway Client)
    # ==========================================
    if user.phone_number:
        sms_message = (
            f"Assetra Security: Your verification code is {otp}. "
            f"IP: {ip_address}. If this wasn't you, secure your account."
        )

        try:
            at_username = getattr(settings, 'AT_USERNAME', 'sandbox')
            at_api_key = getattr(settings, 'AT_API_KEY', 'atsk_2d7c42af1c97dab732786631f714aa99a64e4961983cade49a510c61403165b19705448d')

            recipient_phone = user.phone_number.strip()
            if not recipient_phone.startswith("+"):
                if recipient_phone.startswith("0"):
                    recipient_phone = "+255" + recipient_phone[1:]
                else:
                    recipient_phone = "+" + recipient_phone

            # Select Sandbox vs Live endpoint
            url = "https://api.sandbox.africastalking.com/version1/messaging" if at_username == "sandbox" else "https://api.africastalking.com/version1/messaging"

            payload = urllib.parse.urlencode({
                'username': at_username,
                'to': recipient_phone,
                'message': sms_message
            }).encode('utf-8')

            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded',
                'apiKey': at_api_key
            }

            req = urllib.request.Request(url, data=payload, headers=headers, method='POST')
            with urllib.request.urlopen(req, timeout=10) as response:
                res_data = json.loads(response.read().decode('utf-8'))
                print(f"\n[SMS GATEWAY SUCCESS]: {res_data}\n")

        except Exception as e:
            print(f"\n[SMS GATEWAY ERROR]: {e}")
            # Reliable terminal fallback display
            print("==========================================")
            print(" [SMS FALLBACK CONSOLE DISPLAY]")
            print(f" To Phone : {user.phone_number}")
            print(f" OTP Code : {otp}")
            print("==========================================\n")