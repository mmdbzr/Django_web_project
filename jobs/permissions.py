from rest_framework import permissions


class IsEmployer(permissions.BasePermission):
    """
    فقط کارفرما میتونه Job ایجاد کنه.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and getattr(request.user, "is_employer", False))


class IsSeeker(permissions.BasePermission):
    """
    فقط کارجو میتونه برای شغل Apply کنه.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and getattr(request.user, "is_seeker", False))


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    صاحب شغل (employer) یا اپلیکیشن بتونه اطلاعات خودش رو تغییر بده.
    بقیه فقط Read-Only دسترسی دارن.
    """
    def has_object_permission(self, request, view, obj):
        # درخواست‌های read-only (GET, HEAD, OPTIONS) آزاد هستن
        if request.method in permissions.SAFE_METHODS:
            return True

        # برای Job → صاحب شغل باید باشه
        if hasattr(obj, "user"):
            return obj.user == request.user

        return False


class IsAdmin(permissions.BasePermission):
    """
    فقط ادمین به تمام عملیات ها دسترسی کامل داره.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)