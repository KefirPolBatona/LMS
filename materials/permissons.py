from rest_framework import permissions


class IsAdministrator(permissions.BasePermission):

    def has_permission(self, request, view):
        """
        Проверяет, является ли пользователь администратором.
        """

        return request.user.groups.filter(name='administrator').exists()


class IsTeacher(permissions.BasePermission):

    def has_permission(self, request, view):
        """
        Проверяет, является ли пользователь педагогом.
        """

        return request.user.groups.filter(name='teacher').exists()


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        """
        Проверяет, является ли пользователь владельцем.
        """

        return obj.owner == request.user
