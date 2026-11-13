from django.urls import path
from . import views

app_name = "support"

urlpatterns = [
    # Support & Ticket Endpoints
    path('', views.support_hub, name='support_hub'),
    path('list/', views.user_ticket_list, name='ticket_list'),
    path('new/', views.create_ticket, name='create_ticket'),

    # SEO & Site Verification File Management Endpoints
    path('seo-files/', views.manage_seo_files, name='seo_files_manager'),
    path('seo-files/edit/<int:pk>/', views.edit_seo_file, name='edit_seo_file'),
    path('seo-files/delete/<int:pk>/', views.delete_seo_file, name='delete_seo_file'),
]