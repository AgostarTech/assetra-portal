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

    # Beneficiary dashboard overview
    path(
        "user/",
        views.user_dashboard,
        name="user_dashboard"
    ),

    # Modular client views linked from the sidebar
    path(
        "statements/",
        views.client_statements,
        name="statements"
    ),
    path(
        "documents/",
        views.client_documents,
        name="documents"
    ),
    path(
        "support/",
        views.client_support,
        name="support"
    ),
    path(
        "profile/",
        views.client_profile,
        name="profile"
    ),

    # Admin Control Hub & Management Section
    path(
        "admin-hub/",
        views.admin_dashboard,
        name="admin_dashboard"
    ),
    path(
        "admin-hub/users/",
        views.admin_manage_users,
        name="admin_manage_users"
    ),
    path(
        "admin-hub/groups-permissions/",
        views.admin_groups_permissions,
        name="admin_groups_permissions"
    ),
    path(
        "admin-hub/assets/",
        views.admin_all_assets,
        name="admin_all_assets"
    ),
    path(
        "admin-hub/portfolios/",
        views.admin_client_portfolios,
        name="admin_client_portfolios"
    ),
    path(
        "admin-hub/documents/",
        views.admin_documents_kyc,
        name="admin_documents_kyc"
    ),
    path(
        "admin-hub/tickets/",
        views.admin_support_tickets,
        name="admin_support_tickets"
    ),
    path(
        "admin-hub/audit-logs/",
        views.admin_audit_logs,
        name="admin_audit_logs"
    ),
]