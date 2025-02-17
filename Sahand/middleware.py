from django.utils.timezone import now
from security.models import UserLog, Operation  # Import your model
from django.utils.deprecation import MiddlewareMixin

class UserLogMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        user = request.user if request.user.is_authenticated else None
        ip = self.get_client_ip(request)
        # operation = Operation.objects.filter(url=request.path.rstrip(request.path[-1]))
        UserLog.objects.create(
            method=request.method,
            path=request.path,
            status_code=response.status_code,
            timestamp=now(),
            user=user,
            # operation= operation if operation else None,
            ip_address=ip,
            headers=dict(request.headers)
        )
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
