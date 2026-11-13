from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.views.generic import RedirectView, TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from support.views import serve_verification_file

from accounts import views as accounts_views


urlpatterns = [

    path('<str:filename>', serve_verification_file, name='serve_verification_file'),
    # --------------------------------------------------
    # PUBLIC WEBSITE
    # --------------------------------------------------
    path(
        "",
        TemplateView.as_view(template_name="public/home.html"),
        name="home",
    ),
    path(
        "about/",
        TemplateView.as_view(template_name="public/about.html"),
        name="about",
    ),
    path(
        "solutions/",
        TemplateView.as_view(template_name="public/solutions.html"),
        name="solutions",
    ),
    path(
        "contact/",
        TemplateView.as_view(template_name="public/contact.html"),
        name="contact",
    ),

    # --------------------------------------------------
    # AUTHENTICATION AND REGISTRATION (NAMESPACED)
    # --------------------------------------------------
    path(
        "signup/",
        accounts_views.signup_view,
        name="signup",
    ),

    # Includes login, verify-otp, and other custom account views with namespace 'accounts'
    path(
        "accounts/",
        include(("accounts.urls", "accounts"), namespace="accounts"),
    ),

    # Global Logout endpoint matching the sidebar template request
    path(
        "accounts/logout/",
        auth_views.LogoutView.as_view(next_page="/accounts/login/"),
        name="logout",
    ),

    # --------------------------------------------------
    # FORGOT PASSWORD / PASSWORD RESET
    # --------------------------------------------------
    path(
        "accounts/password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset.html",
            email_template_name="accounts/password_reset_email.html",
            subject_template_name="accounts/password_reset_subject.txt",
            success_url=reverse_lazy("password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "accounts/password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    path(
        "accounts/reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/password_reset_confirm.html",
            success_url=reverse_lazy("password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "accounts/reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),

    # --------------------------------------------------
    # DJANGO ADMIN
    # --------------------------------------------------
    path("admin/", admin.site.urls),

    # --------------------------------------------------
    # DASHBOARD AND PORTAL
    # --------------------------------------------------
    path(
        "dashboard/",
        include("dashboards.urls"),
    ),
    path(
        "portal/",
        RedirectView.as_view(
            url="/dashboard/router/",
            permanent=False,
        ),
        name="portal_redirect",
    ),

    # --------------------------------------------------
    # ASSET MANAGEMENT
    # --------------------------------------------------
    path(
        "assets/",
        include("assets.urls"),
    ),

    # --------------------------------------------------
    # OTHER SYSTEM APPS
    # --------------------------------------------------
    path(
        "documents/",
        include("documents.urls"),
    ),
    path(
        "support/",
        include("support.urls"),
    ),
    path(
        "portfolios/",
        include("portfolios.urls"),
    ),
    path(
        "audit/",
        include("audit.urls"),
    ),
]

# --------------------------------------------------
# MEDIA FILES — DEVELOPMENT ONLY
# --------------------------------------------------
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )