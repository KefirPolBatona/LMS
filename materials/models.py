from django.db import models

from config import settings

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    """
    Модель курса.
    """

    title_course = models.CharField(max_length=350, verbose_name="Название курса")
    description_course = models.TextField(verbose_name="Описание курса", **NULLABLE)
    image_course = models.ImageField(upload_to="image_course/", verbose_name="Превью курса", **NULLABLE)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего изменения")

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="Автор",
        **NULLABLE,
    )

    def __str__(self):
        return self.title_course

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['-id']


class Lesson(models.Model):
    """
    Модель урока.
    """

    title_lesson = models.CharField(max_length=350, verbose_name="Название урока")
    description_lesson = models.TextField(verbose_name="Описание урока", **NULLABLE)
    image_lesson = models.ImageField(upload_to="image_lesson/", verbose_name="Превью урока", **NULLABLE)
    link_video = models.URLField(max_length=550, verbose_name="Ссылка на видео", **NULLABLE)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата последнего изменения")

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс",
        related_name="lessons",
        **NULLABLE,
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="Автор",
        **NULLABLE,
    )

    def __str__(self):
        return self.title_lesson

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['-id']
