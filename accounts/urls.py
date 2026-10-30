
from django.urls import path
from . import views

app_name = "dashboards"

urlpatterns = [
    path("role-router/", views.role_router, name="role_router"),
    path("user/", views.user_dashboard, name="user_dashboard"),
    path("admin/", views.admin_dashboard, name="admin_dashboard"),
]
