from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()


def signup_view(request):
    """Handles standard user registration and defaults to USER role."""
    if request.user.is_authenticated:
        return redirect("role_router")

    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password")

        # Basic input validation
        if not email or not password:
            messages.error(request, "Email and password are required to register.")
            return render(request, "registration/signup.html")

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "An account with this email address already exists.")
            return render(request, "registration/signup.html")

        # Derive a unique username safely
        base_username = email.split('@')[0]
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        # Create user and explicitly assign USER role
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.role = "USER"
        user.save()

        # Log user in directly upon registration
        login(request, user)
        messages.success(request, f"Welcome to the portal, {user.first_name or user.username}!")
        return redirect("role_router")

    return render(request, "registration/signup.html")


def login_view(request):
    """Direct login view bypassing MFA and routing based on role."""
    if request.user.is_authenticated:
        return redirect("role_router")

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            return redirect('role_router')
        else:
            messages.error(request, "Invalid credentials. Please check your username/email and password.")
    else:
        form = AuthenticationForm()

    return render(request, "registration/login.html", {"form": form})