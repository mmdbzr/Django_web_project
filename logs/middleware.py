from datetime import datetime
from logs.models import Log  # مدل Log که بعدا می‌سازیم

class UserActivityLogMiddleware:
    """
    Middleware برای ذخیره فعالیت کاربران
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            Log.objects.create(
                user=request.user,
                path=request.path,
                method=request.method,
                timestamp=datetime.now()
            )

        return response
