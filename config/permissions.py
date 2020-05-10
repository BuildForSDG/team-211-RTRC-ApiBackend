from rest_framework.permissions import BasePermission

class IsSchoolAccount(BasePermission):
    def has_object_permission(self, request, view, obj):
        is_admin_user = False
        if request.user.is_authenticated and request.user.is_admin_user:
            is_admin_user = True
        return is_admin_user


class IsStudentAccount(BasePermission):
    def has_object_permission(self, request, view, obj):
        is_student = False
        if request.user.is_authenticated and request.user.is_student:
            is_student = True
        return is_student
