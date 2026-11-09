from django.urls import path
from . import views

app_name = "support"

urlpatterns = [
    path('', views.support_hub, name='support_hub'),
    path('list/', views.user_ticket_list, name='ticket_list'),
    path('new/', views.create_ticket, name='create_ticket'),
]