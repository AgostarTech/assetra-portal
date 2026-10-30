from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_ticket_list, name='user_ticket_list'),
    path('new/', views.create_ticket, name='create_ticket'),
]
