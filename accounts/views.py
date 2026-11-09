import uuid
import requests
from datetime import timedelta
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model, login, authenticate
from django.utils import timezone
from django.conf import settings
from .utils import send_otp_notifications
from .models import UserSubscription, PaymentTransaction
from .gateway import TanzanianPaymentGateway

User = get_user_model()


# ==========================================================
# ROLE-BASED REDIRECTION (ADMIN vs. USER)
# ==========================================================

@login_required
def role_router(request):
    """
    Redirects authenticated users strictly to Admin or User dashboards.
    """
    user = request.user
    role = (getattr(user, "role", "USER") or "USER").upper()

    if role == "ADMIN" or user.is_staff or user.is_superuser:
        return redirect("dashboards:admin_dashboard")

    return redirect("dashboards:user_dashboard")


# ==========================================================
# USER REGISTRATION
# ==========================================================

def signup_view(request):
    if request.user.is_authenticated:
        return redirect("dashboards:role_router")

    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip().lower()
        phone_number = request.POST.get("phone_number", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not email or not password or not confirm_password:
            messages.error(request, "All required fields, including password confirmation, must be filled.")
            return render(request, "registration/signup.html")

        if len(password) < 8:
            messages.error(request, "Password must contain at least 8 characters.")
            return render(request, "registration/signup.html")

        if password != confirm_password:
            messages.error(request, "Passwords do not match. Please re-enter.")
            return render(request, "registration/signup.html")

        if User.objects.filter(email__iexact=email).exists():
            messages.error(request, "An account with this email address already exists.")
            return render(request, "registration/signup.html")

        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number if phone_number else None
        )

        user.role = "USER"
        user.save(update_fields=["role"])

        # Automatically create free trial subscription upon signup
        UserSubscription.objects.get_or_create(user=user)

        # NOTE: OTP is frozen for now as requested. If you want signup to also bypass OTP, 
        # uncomment the auto-login below and remove the redirect to verify_otp.
        
        # user.generate_otp()
        # send_otp_notifications(user)
        # request.session['pre_otp_user_id'] = user.id
        # request.session.modified = True
        # messages.info(request, "Account created! A verification code has been sent to your email and phone.")
        # return redirect("accounts:verify_otp")

        # Direct login & redirection for signup (optional, mirroring login change):
        login(request, user)
        messages.success(request, f"Account created successfully! Welcome, {user.first_name or user.email}!")
        return redirect("dashboards:role_router")

    return render(request, "registration/signup.html")


# ==========================================================
# USER LOGIN (OTP BYPASSED / FROZEN)
# ==========================================================

def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboards:role_router")

    if request.method == "POST":
        identifier = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(request, username=identifier, password=password)

        if user is not None:
            # Log the user straight in
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.email}!")
            
            # Redirect straight to dashboard via role router
            return redirect("dashboards:role_router")
        else:
            messages.error(request, "Invalid credentials. Please check your email/phone and password.")

    return render(request, "registration/login.html")


# ==========================================================
# OTP VERIFICATION & DIRECT REDIRECTION (FROZEN / UNUSED FOR NOW)
# ==========================================================

def verify_otp_view(request):
    """
    Frozen for now. Kept here in case you want to re-enable OTP functionality later.
    """
    user_id = request.session.get('pre_otp_user_id')
    if not user_id:
        messages.error(request, "Verification session expired. Please sign in again.")
        return redirect("accounts:login")

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return redirect("accounts:login")

    if request.method == "POST":
        entered_code = request.POST.get("otp_code", "").strip()

        if user.is_otp_valid(entered_code):
            user.otp_code = None
            user.otp_created_at = None
            user.save(update_fields=['otp_code', 'otp_created_at'])

            if 'pre_otp_user_id' in request.session:
                del request.session['pre_otp_user_id']
                
            login(request, user)

            messages.success(request, f"Welcome back, {user.first_name or user.email}!")
            return redirect("dashboards:role_router")
        else:
            messages.error(request, "Invalid or expired verification code. Please try again.")

    return render(request, "registration/verify_otp.html")


# ==========================================================
# BILLING & SUBSCRIPTIONS
# ==========================================================

@login_required
def subscription_plans_view(request):
    sub, _ = UserSubscription.objects.get_or_create(user=request.user)
    sub.check_expiration()
    context = {
        "subscription": sub,
        "title": "Account Subscription & Plans"
    }
    return render(request, 'accounts/subscription_plans.html', context)


@login_required
def select_payment_method(request):
    """Step 2: User selects their preferred Tanzanian mobile network or bank with free sandbox simulation."""
    plan = request.GET.get('plan') or request.POST.get('plan')
    if not plan:
        return redirect('accounts:subscription_plans')
        
    amount = 10000.00 if plan == 'MONTHLY' else 100000.00
    
    if request.method == 'POST':
        gateway = request.POST.get('gateway')  # 'MOBILE_MONEY' or 'BANK'
        provider = request.POST.get('provider')  # 'MPESA', 'TIGOPESA', 'AIRTEL', 'HALOPESA', 'NMB', etc.
        phone_number = request.POST.get('phone_number', '').strip()
        
        if gateway == 'MOBILE_MONEY' and not phone_number:
            messages.error(request, "Please enter your mobile money phone number.")
            return redirect(f"{request.path}?plan={plan}")
            
        ref_code = f"AST-{uuid.uuid4().hex[:10].upper()}"
        
        PaymentTransaction.objects.create(
            user=request.user,
            reference_code=ref_code,
            amount=amount,
            gateway=gateway,
            plan_purchased=plan,
            is_successful=False
        )
        
        # Trigger free simulation gateway request
        gateway_res = TanzanianPaymentGateway.request_mno_checkout(phone_number, amount, ref_code, provider)
        messages.success(request, f"{gateway_res['message']} [Sandbox Mode]")
        
        context = {
            "plan": plan,
            "amount": amount,
            "ref_code": ref_code,
            "simulation_mode": True,
            "title": "Complete Simulated Checkout"
        }
        return render(request, 'accounts/payment_checkout.html', context)

    context = {
        "plan": plan,
        "amount": amount,
        "title": "Select Payment Method & Provider"
    }
    return render(request, 'accounts/payment_checkout.html', context)


@login_required
def initiate_payment(request):
    """Initiates payment transaction log."""
    if request.method == 'POST':
        plan = request.POST.get('plan')
        gateway = request.POST.get('gateway')
        amount = 10000.00 if plan == 'MONTHLY' else 100000.00
        ref_code = f"AST-{uuid.uuid4().hex[:10].upper()}"

        PaymentTransaction.objects.create(
            user=request.user,
            reference_code=ref_code,
            amount=amount,
            gateway=gateway,
            plan_purchased=plan,
            is_successful=False
        )
        messages.info(request, f"Payment request initiated for {amount:,.2f} TZS.")
        return redirect('accounts:subscription_plans')

    return redirect('accounts:subscription_plans')


@login_required
def simulate_payment_success(request, reference_code):
    """Instantly simulates payment completion for free testing in sandbox mode."""
    try:
        tx = PaymentTransaction.objects.get(reference_code=reference_code, user=request.user)
        tx.is_successful = True
        tx.save()

        # Activate user subscription immediately
        sub, _ = UserSubscription.objects.get_or_create(user=request.user)
        sub.plan_type = tx.plan_purchased
        sub.status = 'ACTIVE'
        sub.is_locked = False
        
        days_to_add = 30 if tx.plan_purchased == 'MONTHLY' else 365
        sub.expiry_date = timezone.now() + timedelta(days=days_to_add)
        sub.save()

        messages.success(request, f"Sandbox payment of {tx.amount:,.2f} TZS confirmed successfully! Your portal access is now active.")
    except PaymentTransaction.DoesNotExist:
        messages.error(request, "Transaction reference not found.")

    return redirect('accounts:subscription_plans')