from rest_framework.permissions import BasePermission


class IsCollector(BasePermission):
    def has_permission(self, request):
        if request.user.is_collector and request.user.is_authenticated:
            return True
        return False


class IsUser(BasePermission):
    def has_permission(self, request):
        if request.user.is_user and request.user.is_authenticated:
            return True
        return False

