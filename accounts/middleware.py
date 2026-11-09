# middleware.py
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from .models import UserSubscription

class SubscriptionCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.user.is_superuser:
            # Exempt logout, static files, and the billing/payment pages from being locked
            exempt_urls = [
                reverse('accounts:subscription_plans'),
                reverse('accounts:process_payment'),
                reverse('logout'),
            ]
            if request.path not in exempt_urls and not request.path.startswith('/static/'):
                sub, created = UserSubscription.objects.get_or_create(user=request.user)
                if sub.check_expiration():
                    return redirect('accounts:subscription_plans')
                    
        response = self.get_response(request)
        return response