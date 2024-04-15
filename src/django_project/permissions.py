from rest_framework import permissions

from src.core._shared.infrastructure.auth.jwt_auth_service import JwtAuthService


class IsAuthenticated(permissions.BasePermission):
    message = 'Invalid or expired token.'

    def has_permission(self, request, view):
        token = request.headers.get('Authorization', '')
        if not JwtAuthService(token).is_authenticated():
            return False
        return True


class IsAdmin(permissions.BasePermission):
    message = 'User does not have admin privileges.'

    def has_permission(self, request, view):
        token = request.headers.get('Authorization', '')
        if not JwtAuthService(token).has_role('admin'):
            return False
        return True
