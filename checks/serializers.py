from rest_framework import serializers

from checks.models import Question, Answer, Choice


class QuestionSerializer(serializers.ModelSerializer):
    count_answers = serializers.SerializerMethodField()
    answers = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = '__all__'

    def get_count_answers(self, instance):
        """
        Возвращает количество вариантов ответа тестового задания.
        """

        return instance.answers.all().count()

    def get_answers(self, instance):
        """
        Возвращает все варианты ответа для тестового задания.
        """

        return [answer.answer for answer in instance.answers.all()]


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = '__all__'


class ChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Choice
        fields = ('student', 'question', 'answer',)
