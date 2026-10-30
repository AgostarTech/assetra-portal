
from django.urls import path
from . import views

app_name = "dashboards"

urlpatterns = [
    path("", views.role_router, name="role_router"),
    path("user/", views.user_dashboard, name="user_dashboard"),
    path("admin-hub/", views.admin_dashboard, name="admin_dashboard"),
    path(
        "admin-hub/users/",
        views.admin_manage_users,
        name="admin_manage_users",
    ),
]
