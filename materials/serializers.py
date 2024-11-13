from rest_framework import serializers

from materials.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    count_lesson = serializers.SerializerMethodField()
    lessons = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_count_lesson(self, instance):
        """
        Возвращает количество уроков курса.
        """

        return instance.lessons.all().count()

    def get_lessons(self, instance):
        """
        Возвращает все уроки курса.
        """

        return [lesson.title_lesson for lesson in instance.lessons.all()]


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'
