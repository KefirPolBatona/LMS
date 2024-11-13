import nested_admin
from django.contrib import admin

from checks.models import Answer, Question, Choice


class AnswerInline(nested_admin.NestedTabularInline):
    model = Answer


class QuestionInline(nested_admin.NestedStackedInline):
    model = Question
    inlines = [AnswerInline]


class QuestionAdmin(nested_admin.NestedModelAdmin):
    model = Question
    fields = ('lesson', 'question',)
    list_display = ('pk', 'question', 'course', 'lesson', 'owner',)

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'owner', None) is None:
            obj.owner = request.user
        obj.save()


class ChoiceAdmin(nested_admin.NestedModelAdmin):
    model = Choice
    fields = ('question', 'answer',)
    list_display = ('pk', 'student', 'question', 'answer', 'right_answer',)

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'student', None) is None:
            obj.student = request.user
        obj.save()


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    fields = ('question', 'answer', 'right_answer',)
    list_display = (
        'id', 'answer', 'right_answer',
        'question', 'owner',
    )

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'owner', None) is None:
            obj.owner = request.user
        obj.save()
