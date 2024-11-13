from rest_framework import viewsets, generics

from rest_framework.permissions import IsAuthenticated

from materials.models import Course, Lesson
from materials.paginators import MaterialsPagination
from materials.permissons import IsAdministrator, IsOwner, IsTeacher
from materials.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """
    CRUD курса.
    """

    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = MaterialsPagination

    def get_permissions(self):
        """
        Определяет права доступа к эндпоинтам.
        """

        if self.action == 'create':
            self.permission_classes = (IsAdministrator | IsTeacher,)
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = (IsAdministrator | IsOwner,)
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = (IsAuthenticated,)

        return super().get_permissions()

    def perform_create(self, serializer):
        """
        Привязывает пользователя к создаваемому им курсу.
        """

        serializer.save(owner=self.request.user)


class LessonCreateAPIView(generics.CreateAPIView):
    """
    Эндпоинт создания урока пользователем с правами доступа.
    """

    serializer_class = LessonSerializer
    permission_classes = [IsAdministrator | IsTeacher]

    def perform_create(self, serializer):
        """
        Привязывает пользователя к создаваемому им уроку.
        """

        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    """
    Эндпоинт просмотра списка уроков.
    """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = MaterialsPagination
    permission_classes = [IsAuthenticated]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """
    Эндпоинт просмотра урока.
    """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """
    Эндпоинт редактирования урока пользователем с правами доступа.
    """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAdministrator | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """
    Эндпоинт удаления урока пользователем с правами доступа.
    """

    queryset = Lesson.objects.all()
    permission_classes = [IsAdministrator | IsOwner]
