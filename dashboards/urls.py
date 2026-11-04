
from django.urls import path
from . import views

app_name = "dashboards"

urlpatterns = [
    # Centralized role-based routing
    path(
        "",
        views.role_router,
        name="role_router"
    ),

    # Beneficiary dashboard
    path(
        "user/",
        views.user_dashboard,
        name="user_dashboard"
    ),

    # Admin dashboard
    path(
        "admin-hub/",
        views.admin_dashboard,
        name="admin_dashboard"
    ),

    # Admin user management
    path(
        "admin-hub/users/",
        views.admin_manage_users,
        name="admin_manage_users"
    ),
]
