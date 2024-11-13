from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson
from users.models import User


class MaterialsTestCase(APITestCase):
    """
    Тестирование CRUD курсов и уроков.
    """

    def setUp(self) -> None:
        self.user = User.objects.create(email='test888@gmail.com')
        self.administrator = User.objects.create(email='test777@gmail.com')
        self.owner = User.objects.create(email='9232485@gmail.com')
        self.group = Group.objects.create(name='administrator')
        self.administrator.groups.add(self.group)
        self.course = Course.objects.create(title_course='Тестовый курс', owner=self.owner)
        self.lesson = Lesson.objects.create(title_lesson='Тестовый урок', course=self.course, owner=self.owner)
        self.new_lesson = Lesson.objects.create(title_lesson='Тестовый урок', course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.owner)

    def test_course_create(self):
        """
        Тестирование: создания курса, пользователь не авторизован.
        """

        self.client.force_authenticate(user=None)
        url = reverse("materials:courses-list")
        data = {
            "title_course": "Тестовый курс",
        }
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_course_create_authenticate(self):
        """
        Тестирование: создания курса, пользователь авторизован.
        """

        url = reverse("materials:courses-list")
        data = {
            "title_course": "Тестовый курс",
        }
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_course_create_administrator(self):
        """
        Тестирование: создание куса, пользователь администратор.
        """

        self.client.force_authenticate(user=self.administrator)
        url = reverse("materials:courses-list")
        data = {
            "title_course": "Тестовый курс",
        }
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_course_list(self):
        """
        Тестирование: вывод списка курсов, пользователь не авторизован.
        """

        self.client.force_authenticate(user=None)
        url = reverse('materials:courses-list')
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_course_list_authenticate(self):
        """
        Тестирование: вывод списка курсов, пользователь авторизован.
        """

        url = reverse('materials:courses-list')
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_course_list_administrator(self):
        """
        Тестирование: вывод списка курсов, пользователь администратор.
        """

        self.client.force_authenticate(user=self.administrator)
        url = reverse('materials:courses-list')
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_course_retrieve(self):
        """
        Тестирование: вывод одного курса, пользователь не авторизован.
        """

        self.client.force_authenticate(user=None)
        url = reverse("materials:courses-detail", args=(self.course.pk,))
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_course_retrieve_authenticate(self):
        """
        Тестирование: вывод одного курса, пользователь авторизован.
        """

        url = reverse("materials:courses-detail", args=(self.course.pk,))
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_course_retrieve_administrator(self):
        """
        Тестирование: вывод одного курса, пользователь модератор.
        """

        self.client.force_authenticate(user=self.administrator)
        url = reverse("materials:courses-detail", args=(self.course.pk,))
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_course_update(self):
        """
        Тестирование: редактирование курса, пользователь не авторизован.
        """

        self.client.force_authenticate(user=None)
        url = reverse("materials:courses-detail", args=(self.course.pk,))
        data = {
            'title_course': 'Измененный тестовый курс',
        }
        response = self.client.patch(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_course_update_authenticate(self):
        """
        Тестирование: редактирование курса, пользователь авторизован.
        """

        url = reverse("materials:courses-detail", args=(self.course.pk,))
        data = {
            'title_course': 'Измененный тестовый курс',
        }
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(
            data.get('title_course'),
            'Измененный тестовый курс'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_course_update_administrator(self):
        """
        Тестирование: редактирование курса, пользователь администратор.
        """

        self.client.force_authenticate(user=self.administrator)
        url = reverse("materials:courses-detail", args=(self.course.pk,))
        data = {
            'title_course': 'Измененный тестовый курс',
        }
        response = self.client.patch(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_course_delete(self):
        """
        Тестирование: удаление курса, пользователь не авторизован.
        """

        self.client.force_authenticate(user=None)
        url = reverse("materials:courses-detail", args=(self.course.pk,))
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_course_delete_authenticate(self):
        """
        Тестирование: удаление курса, пользователь авторизован.
        """

        url = reverse("materials:courses-detail", args=(self.course.pk,))
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_course_delete_administrator(self):
        """
        Тестирование: удаление курса, пользователь администратор.
        """

        self.client.force_authenticate(user=self.administrator)
        url = reverse("materials:courses-detail", args=(self.course.pk,))
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_lesson_create(self):
        """
        Тестирование: создания урока, пользователь не авторизован.
        """

        self.client.force_authenticate(user=None)
        url = reverse("materials:lesson-create")
        data = {
            "title_lesson": "Тестовый урок",
        }
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_lesson_create_authenticate(self):
        """
        Тестирование: создания урока, пользователь авторизован.
        """

        url = reverse("materials:lesson-create")
        data = {
            "title_lesson": "Тестовый урок",
        }
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

    def test_lesson_create_administrator(self):
        """
        Тестирование: создание урока, пользователь администратор.
        """

        self.client.force_authenticate(user=self.administrator)
        url = reverse("materials:lesson-create")
        data = {
            "title_lesson": "Тестовый урок",
        }
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_lesson_list(self):
        """
        Тестирование: вывод списка уроков, пользователь не авторизован.
        """

        self.client.force_authenticate(user=None)
        url = reverse('materials:lesson-list')
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_lesson_list_authenticate(self):
        """
        Тестирование: вывод списка уроков, пользователь авторизован.
        """

        url = reverse('materials:lesson-list')
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_lesson_list_administrator(self):
        """
        Тестирование: вывод списка уроков, пользователь администратор.
        """

        self.client.force_authenticate(user=self.administrator)
        url = reverse('materials:lesson-list')
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_lesson_retrieve(self):
        """
        Тестирование: вывод одного урока, пользователь не авторизован.
        """

        self.client.force_authenticate(user=None)
        url = reverse("materials:lesson-get", args=(self.lesson.pk,))
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_lesson_retrieve_authenticate(self):
        """
        Тестирование: вывод одного урока, пользователь авторизован.
        """

        url = reverse("materials:lesson-get", args=(self.lesson.pk,))
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_lesson_retrieve_administrator(self):
        """
        Тестирование: вывод одного урока, пользователь модератор.
        """

        self.client.force_authenticate(user=self.administrator)
        url = reverse("materials:lesson-get", args=(self.lesson.pk,))
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_lesson_update(self):
        """
        Тестирование: редактирование урока, пользователь не авторизован.
        """

        self.client.force_authenticate(user=None)
        url = reverse("materials:lesson-update", args=(self.lesson.pk,))
        data = {
            'title_lesson': 'Измененный тестовый урок',
        }
        response = self.client.patch(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_lesson_update_authenticate(self):
        """
        Тестирование: редактирование урока, пользователь авторизован.
        """

        url = reverse("materials:lesson-update", args=(self.lesson.pk,))
        data = {
            'title_lesson': 'Измененный тестовый урок',
        }
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(
            data.get('title_lesson'),
            'Измененный тестовый урок'
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_lesson_update_administrator(self):
        """
        Тестирование: редактирование урока, пользователь администратор.
        """

        self.client.force_authenticate(user=self.administrator)
        url = reverse("materials:lesson-update", args=(self.lesson.pk,))
        data = {
            'title_lesson': 'Измененный тестовый урок',
        }
        response = self.client.patch(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_lesson_delete(self):
        """
        Тестирование: удаление урока, пользователь не авторизован.
        """

        self.client.force_authenticate(user=None)
        url = reverse("materials:lesson-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

    def test_lesson_delete_authenticate(self):
        """
        Тестирование: удаление урока, пользователь авторизован.
        """

        url = reverse("materials:lesson-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_lesson_delete_administrator(self):
        """
        Тестирование: удаление урока, пользователь администратор.
        """

        self.client.force_authenticate(user=self.administrator)
        url = reverse("materials:lesson-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
