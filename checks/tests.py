from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from checks.models import Question, Answer, Choice
from materials.models import Course, Lesson
from users.models import User


class ChecksTestCase(APITestCase):
    """
    Тестирование CRUD тестовых заданий и вариантов ответа.
    """

    def setUp(self) -> None:
        self.user = User.objects.create(email='test888@gmail.com')
        self.administrator = User.objects.create(email='test777@gmail.com')
        self.owner = User.objects.create(email='9232485@gmail.com')
        self.group = Group.objects.create(name='administrator')
        self.administrator.groups.add(self.group)

        self.course = Course.objects.create(
            title_course='Тестовый курс',
            owner=self.owner
        )
        self.lesson = Lesson.objects.create(
            title_lesson='Тестовый урок',
            course=self.course,
            owner=self.owner
        )
        self.new_lesson = Lesson.objects.create(
            title_lesson='Тестовый урок',
            course=self.course,
            owner=self.user
        )

        self.question = Question.objects.create(
            question='Тестовый вопрос',
            lesson=self.lesson,
            course=self.course,
            owner=self.owner
        )
        self.answer = Answer.objects.create(
            answer='Тестовый ответ',
            question=self.question,
            owner=self.owner
        )
        self.choice = Choice.objects.create(
            question=self.question,
            answer=self.answer,
            student=self.owner
        )

        self.client.force_authenticate(user=self.owner)

    def test_question_create(self):
        """
        Тестирование: создание тестового вопроса, пользователь не авторизован.
        """

        self.client.force_authenticate(user=None)
        url = reverse("checks:questions-list")
        data = {
            "question": "Тестовый вопрос",
        }
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_question_create_authenticate(self):
        """
        Тестирование: создания тестового вопроса, пользователь авторизован.
        """

        url = reverse("checks:questions-list")
        data = {
            "question": "Тестовый вопрос",
        }
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_question_list(self):
        """
        Тестирование: вывод списка тестовых вопросов, пользователь не авторизован.
        """

        self.client.force_authenticate(user=None)
        url = reverse('checks:questions-list')
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_question_list_authenticate(self):
        """
        Тестирование: вывод списка тестовых вопросов, пользователь авторизован.
        """

        url = reverse('checks:questions-list')
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_question_list_administrator(self):
        """
        Тестирование: вывод списка тестовых вопросов, пользователь администратор.
        """

        self.client.force_authenticate(user=self.administrator)
        url = reverse('checks:questions-list')
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_question_retrieve(self):
        """
        Тестирование: вывод одного тестового вопроса, пользователь не авторизован.
        """

        self.client.force_authenticate(user=None)
        url = reverse("checks:questions-detail", args=(self.question.pk,))
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_question_retrieve_authenticate(self):
        """
        Тестирование: вывод одного тестового вопроса, пользователь авторизован.
        """

        url = reverse("checks:questions-detail", args=(self.question.pk,))
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_question_retrieve_administrator(self):
        """
        Тестирование: вывод одного тестового вопроса, пользователь модератор.
        """

        self.client.force_authenticate(user=self.administrator)
        url = reverse("checks:questions-detail", args=(self.question.pk,))
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_question_update(self):
        """
        Тестирование: редактирование тестового вопроса, пользователь не авторизован.
        """

        self.client.force_authenticate(user=None)
        url = reverse("checks:questions-detail", args=(self.question.pk,))
        data = {
            "question": "Тестовый вопрос",
        }
        response = self.client.patch(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_question_update_authenticate(self):
        """
        Тестирование: редактирование тестового вопроса, пользователь авторизован.
        """

        url = reverse("checks:questions-detail", args=(self.question.pk,))
        data = {
            "question": "Измененный тестовый вопрос",
        }
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(
            data.get('question'),
            "Измененный тестовый вопрос"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_question_update_administrator(self):
        """
        Тестирование: редактирование тестового вопроса, пользователь администратор.
        """

        self.client.force_authenticate(user=self.administrator)
        url = reverse("checks:questions-detail", args=(self.question.pk,))
        data = {
            "question": "Тестовый вопрос",
        }
        response = self.client.patch(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_question_delete(self):
        """
        Тестирование: удаление тестового вопроса, пользователь не авторизован.
        """

        self.client.force_authenticate(user=None)
        url = reverse("checks:questions-detail", args=(self.question.pk,))
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_question_delete_authenticate(self):
        """
        Тестирование: удаление тестового вопроса, пользователь авторизован.
        """

        url = reverse("checks:questions-detail", args=(self.question.pk,))
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_question_delete_administrator(self):
        """
        Тестирование: удаление тестового вопроса, пользователь администратор.
        """

        self.client.force_authenticate(user=self.administrator)
        url = reverse("checks:questions-detail", args=(self.question.pk,))
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_answer_create(self):
        """
        Тестирование: создания ответа, пользователь не авторизован.
        """

        self.client.force_authenticate(user=None)
        url = reverse("checks:answers-list")
        data = {
            "answer": "Тестовый ответ",
        }
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_answer_create_authenticate(self):
        """
        Тестирование: создания ответа, пользователь авторизован.
        """

        url = reverse("checks:answers-list")
        data = {
            "answer": "Тестовый ответ",
        }
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_answer_list(self):
        """
        Тестирование: вывод списка ответов, пользователь не авторизован.
        """

        self.client.force_authenticate(user=None)
        url = reverse('checks:answers-list')
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_answer_list_authenticate(self):
        """
        Тестирование: вывод списка ответов, пользователь авторизован.
        """

        url = reverse('checks:answers-list')
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_answer_list_administrator(self):
        """
        Тестирование: вывод списка ответов, пользователь администратор.
        """

        self.client.force_authenticate(user=self.administrator)
        url = reverse('checks:answers-list')
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_answer_retrieve(self):
        """
        Тестирование: вывод одного ответа, пользователь не авторизован.
        """

        self.client.force_authenticate(user=None)
        url = reverse("checks:answers-detail", args=(self.answer.pk,))
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_answer_retrieve_authenticate(self):
        """
        Тестирование: вывод одного ответа, пользователь авторизован.
        """

        url = reverse("checks:answers-detail", args=(self.answer.pk,))
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_answer_retrieve_administrator(self):
        """
        Тестирование: вывод одного ответа, пользователь модератор.
        """

        self.client.force_authenticate(user=self.administrator)
        url = reverse("checks:answers-detail", args=(self.answer.pk,))
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_answer_update(self):
        """
        Тестирование: редактирование ответа, пользователь не авторизован.
        """

        self.client.force_authenticate(user=None)
        url = reverse("checks:answers-detail", args=(self.answer.pk,))
        data = {
            'answer': 'Измененный тестовый ответ',
        }
        response = self.client.patch(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_answer_update_authenticate(self):
        """
        Тестирование: редактирование ответа, пользователь авторизован.
        """

        url = reverse("checks:answers-detail", args=(self.answer.pk,))
        data = {
            'answer': 'Измененный тестовый ответ',
        }
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(
            data.get('answer'),
            'Измененный тестовый ответ'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_answer_update_administrator(self):
        """
        Тестирование: редактирование ответа, пользователь администратор.
        """

        self.client.force_authenticate(user=self.administrator)
        url = reverse("checks:answers-detail", args=(self.answer.pk,))
        data = {
            'answer': 'Измененный тестовый ответ',
        }
        response = self.client.patch(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_answer_delete(self):
        """
        Тестирование: удаление ответа, пользователь не авторизован.
        """

        self.client.force_authenticate(user=None)
        url = reverse("checks:answers-detail", args=(self.answer.pk,))
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_answer_delete_authenticate(self):
        """
        Тестирование: удаление ответа, пользователь авторизован.
        """

        url = reverse("checks:answers-detail", args=(self.answer.pk,))
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_answer_delete_administrator(self):
        """
        Тестирование: удаление ответа, пользователь администратор.
        """

        self.client.force_authenticate(user=self.administrator)
        url = reverse("checks:answers-detail", args=(self.answer.pk,))
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_choice_create(self):
        """
        Тестирование: выбор ответа, пользователь не авторизован.
        """

        self.client.force_authenticate(user=None)
        url = reverse("checks:choice-create")
        data = {
            "answer": "Тестовый ответ",
        }
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_choice_create_authenticate(self):
        """
        Тестирование: выбор ответа, неверный запрос.
        """

        url = reverse("checks:choice-create")
        data = {
            "question": 1,
            "answer": 1,
        }
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_choice_list(self):
        """
        Тестирование: вывод списка ответов, пользователь не авторизован.
        """

        self.client.force_authenticate(user=None)
        url = reverse('checks:choice-list')
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_choice_list_authenticate(self):
        """
        Тестирование: вывод списка ответов, пользователь авторизован.
        """

        url = reverse('checks:choice-list')
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_choice_list_administrator(self):
        """
        Тестирование: вывод списка ответов, пользователь администратор.
        """

        self.client.force_authenticate(user=self.administrator)
        url = reverse('checks:choice-list')
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
