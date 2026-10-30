from .models import AuditLog

class AuditLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")

        response = self.get_response(request)

        if request.method in ["POST", "PUT", "DELETE"]:
            user = request.user if request.user.is_authenticated else None
            path = request.path
            if not path.startswith("/static/"):
                action = f"{request.method} Request"
                details = f"Path: {path} | Status Code: {response.status_code}"
                log = AuditLog(user=user, action=action, path=path, ip_address=ip, details=details)
                log.fn_locked = True
                log.save()
                log.fn_locked = False

        return response

