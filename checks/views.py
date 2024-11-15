from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from checks.forms import ChoiceForm
from checks.models import Question, Answer, Choice
from materials.permissons import IsAdministrator, IsOwner, IsTeacher
from checks.serializers import QuestionSerializer, AnswerSerializer, ChoiceSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    """
    CRUD тестового задания.
    """

    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

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
        Привязывает пользователя к создаваемому им тестовому заданию.
        """

        serializer.save(owner=self.request.user)


class AnswerViewSet(viewsets.ModelViewSet):
    """
    CRUD варианта ответа на тестовое задание.
    """

    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()

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
        Привязывает пользователя к создаваемому им варианту ответа.
        """

        serializer.save(owner=self.request.user)


class ChoiceCreateAPIView(generics.CreateAPIView):
    """
    Эндпоинт создания выбора ответа.
    """

    serializer_class = ChoiceSerializer
    permission_classes = [IsAuthenticated]
    form_class = ChoiceForm

    def perform_create(self, serializer):
        """
        Привязывает студента к выбранному ответу.
        """

        serializer.save(student=self.request.user)


class ChoiceListAPIView(generics.ListAPIView):
    """
    Эндпоинт просмотра списка выбранных ответов.
    """

    serializer_class = ChoiceSerializer
    queryset = Choice.objects.all()
    permission_classes = [IsAuthenticated]
