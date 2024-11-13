from rest_framework import viewsets

from users.models import User
from users.permissons import UserPermission

from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    CRUD пользователя.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [UserPermission]
