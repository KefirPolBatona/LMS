from django.db import models

from config import settings
from materials.models import Lesson

NULLABLE = {"blank": True, "null": True}


class Question(models.Model):
    """
    Модель тестового задания по теме урока.
    """

    question = models.CharField(max_length=550, verbose_name="Тестовый вопрос")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="Автор",
        related_name="questions",
        **NULLABLE,
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        verbose_name="Урок",
        related_name="questions",
    )
    course = models.CharField(max_length=550, verbose_name="Курс", **NULLABLE,)

    def __str__(self):
        return f"Тестовый вопрос ({self.pk}): {self.question}"

    class Meta:
        verbose_name = "Тестовое задание"
        verbose_name_plural = "Тестовые задания"
        ordering = ['-id']

    def save(self, *args, **kwargs):
        """
        Определяет и сохраняет поле course.
        """

        if self.course is None:
            self.course = Lesson.objects.all().get(title_lesson=self.lesson).course
        return super(Question, self).save(*args, **kwargs)


class Answer(models.Model):
    """
    Модель варианта ответа для тестового задания.
    """

    answer = models.CharField(max_length=550, verbose_name="Вариант ответа")
    right_answer = models.BooleanField(verbose_name="Признак правильного ответа", default=False)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="Автор",
        related_name="answers",
        **NULLABLE,
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name="Тестовое задание",
        related_name="answers",
    )

    def __str__(self):
        return self.answer

    class Meta:
        verbose_name = "Вариант ответа"
        verbose_name_plural = "Варианты ответов"
        ordering = ['-id']


class Choice(models.Model):
    """
    Модель выбора ответа в тестовом задании.
    """

    right_answer = models.BooleanField(verbose_name="Ответ выбран верно", default=False)
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Студент",
        related_name="choices",
        **NULLABLE,
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name="Тестовое задание",
        related_name="choices",
    )
    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        verbose_name="Выбранный ответ",
        related_name="choices",
    )

    def __str__(self):
        return f"Ответ ({self.answer}) верный: {self.right_answer}"

    class Meta:
        verbose_name = "Проверка знаний"
        verbose_name_plural = "Проверки знаний"
        ordering = ['-id']

    def save(self, *args, **kwargs):
        """
        Проверяет правильность ответа.
        Сохраняет True, если ответ верный.
        """

        if Answer.objects.all().get(answer=self.answer).right_answer is True:
            self.right_answer = True
        return super(Choice, self).save(*args, **kwargs)

