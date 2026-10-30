
from django.http import HttpResponse

class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Toggle maintenance mode state here
        self.maintenance_active = False

    def __call__(self, request):
        if self.maintenance_active and not request.user.is_staff:
            return HttpResponse("""
            <div style="font-family: sans-serif; text-align: center; padding: 50px; background: #1a1a1a; color: #fff; height: 100vh;">
                <h1 style="color: #cfa76e; font-size: 32px;">System Maintenance in Progress</h1>
                <p style="color: #aaa; font-size: 16px;">Our portfolio management platform is currently undergoing scheduled updates. Please check back shortly.</p>
            </div>
            """, status=503)
        
        response = self.get_response(request)
        return response
