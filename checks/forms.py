from django.forms import ModelForm
from django.shortcuts import render

from .models import Choice, Answer


class ChoiceForm(ModelForm):
    class Meta:
        model = Choice
        fields = ['question', 'answer']

    def get_form(self, request):
        question = request.POST.get("question")
        answer = Answer.objects.all()

        if request.method == "POST":
            answer = answer.filter(question=question)

        context_data = {
            'answer': answer
        }

        return render(request, context_data)
