from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()


# ==========================================================
# ROLE-BASED REDIRECTION
# ==========================================================

@login_required
def role_router(request):
    """
    Redirect authenticated users to their respective dashboards
    based on their assigned roles.
    """

    user = request.user
    role = (getattr(user, "role", "") or "").upper()

    if role == "ADMIN":
        return redirect("admin:index")

    elif role == "MANAGER":
        return redirect("dashboards:manager_dashboard")

    elif role in ["HELP_DESK", "HELPDESK"]:
        return redirect("dashboards:helpdesk_dashboard")

    elif role in ["USER", "BENEFICIARY"]:
        return redirect("dashboards:user_dashboard")

    messages.error(
        request,
        "Your account role is not configured. Please contact the administrator."
    )

    return redirect("accounts:login")


# ==========================================================
# USER REGISTRATION
# ==========================================================

def signup_view(request):
    """
    Handles standard user registration.
    Newly registered users receive the USER role by default.
    """

    if request.user.is_authenticated:
        return redirect("dashboards:role_router")

    if request.method == "POST":

        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")

        # Validate required fields
        if not email or not password:
            messages.error(
                request,
                "Email and password are required to register."
            )
            return render(
                request,
                "registration/signup.html"
            )

        # Validate password length
        if len(password) < 8:
            messages.error(
                request,
                "Password must contain at least 8 characters."
            )
            return render(
                request,
                "registration/signup.html"
            )

        # Check whether email already exists
        if User.objects.filter(email__iexact=email).exists():
            messages.error(
                request,
                "An account with this email address already exists."
            )
            return render(
                request,
                "registration/signup.html"
            )

        # Generate a unique username
        base_username = email.split("@")[0]
        username = base_username
        counter = 1

        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        # Create the new user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        # Assign default beneficiary/user role
        user.role = "USER"
        user.save(update_fields=["role"])

        # Authenticate newly registered user
        login(request, user)

        messages.success(
            request,
            f"Welcome to the portal, {user.first_name or user.username}!"
        )

        return redirect("dashboards:role_router")

    return render(
        request,
        "registration/signup.html"
    )


# ==========================================================
# USER LOGIN
# ==========================================================

def login_view(request):
    """
    Handles user authentication and redirects authenticated
    users according to their assigned roles.
    """

    if request.user.is_authenticated:
        return redirect("dashboards:role_router")

    if request.method == "POST":

        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():

            user = form.get_user()

            login(request, user)

            messages.success(
                request,
                f"Welcome back, {user.first_name or user.username}!"
            )

            return redirect("dashboards:role_router")

        else:
            messages.error(
                request,
                "Invalid credentials. Please check your username/email and password."
            )

    else:
        form = AuthenticationForm()

    return render(
        request,
        "registration/login.html",
        {"form": form}
    )