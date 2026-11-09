from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('subscription/plans/', views.subscription_plans_view, name='subscription_plans'),
    path('subscription/pay/', views.initiate_payment, name='initiate_payment'),
    path('subscription/checkout/', views.select_payment_method, name='select_payment_method'),
    path('subscription/simulate-success/<str:reference_code>/', views.simulate_payment_success, name='simulate_payment_success'),
]