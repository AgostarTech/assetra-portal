
from django.urls import path
from . import views

urlpatterns = [
    path('export/csv/', views.export_audit_logs_csv, name='export_audit_logs_csv'),
]
