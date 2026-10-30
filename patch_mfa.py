
import os

model_path = "accounts/models.py"
with open(model_path, "r", encoding="utf-8") as f:
    content = f.read()

if "totp_secret" not in content:
    content = content.replace("class CustomUser(AbstractUser):", "class CustomUser(AbstractUser):\n    totp_secret = models.CharField(max_length=64, blank=True, null=True)\n    is_mfa_enabled = models.BooleanField(default=False)\n")
    with open(model_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated accounts/models.py successfully.")

views_path = "accounts/views.py"
mfa_code = """
import pyotp
import qrcode
import io
import base64
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def setup_mfa(request):
    user = request.user
    if not user.totp_secret:
        user.totp_secret = pyotp.random_base32()
        user.save()

    totp = pyotp.TOTP(user.totp_secret)
    provisioning_uri = totp.provisioning_uri(name=user.email, issuer_name="Asset Portal Enterprise")

    img = qrcode.make(provisioning_uri)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_image = base64.b64encode(buffer.getvalue()).decode()

    if request.method == "POST":
        token = request.POST.get("token")
        if totp.verify(token):
            user.is_mfa_enabled = True
            user.save()
            messages.success(request, "Multi-Factor Authentication successfully enabled.")
            return redirect("user_dashboard")
        else:
            messages.error(request, "Invalid authentication code. Please try again.")

    return render(request, "accounts/setup_mfa.html", {"qr_image": qr_image, "is_mfa_enabled": user.is_mfa_enabled})
"""

with open(views_path, "a", encoding="utf-8") as f:
    f.write(mfa_code)
print("Updated accounts/views.py successfully.")

