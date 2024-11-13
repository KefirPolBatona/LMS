from rest_framework import permissions


class UserPermission(permissions.BasePermission):
    """
    Предоставляет права доступа для регистрации неавторизованному пользователю.
    """

    def has_permission(self, request, view):
        if view.action == 'create':
            return True
        else:
            return request.user.is_authenticated
