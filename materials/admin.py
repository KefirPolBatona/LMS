from django.contrib import admin

from materials.models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    fields = ('title_course', 'description_course', 'image_course',)
    list_display = ('id', 'title_course', 'owner',)

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'owner', None) is None:
            obj.owner = request.user
        obj.save()


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    fields = ('course', 'title_lesson', 'description_lesson', 'image_lesson', 'link_video',)
    list_display = (
        'id', 'title_lesson', 'description_lesson',
        'updated_at', 'course', 'owner',
    )

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'owner', None) is None:
            obj.owner = request.user
        obj.save()
