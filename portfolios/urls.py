
from django.urls import path
from . import views

app_name = "portfolios"

urlpatterns = [
    path("", views.portfolio_dashboard, name="dashboard"),
    path("statement/", views.portfolio_statement, name="statement"),
]
