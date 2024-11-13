from django.urls import path

from checks.apps import ChecksConfig

from rest_framework.routers import DefaultRouter

from checks.views import QuestionViewSet, AnswerViewSet, ChoiceCreateAPIView, ChoiceListAPIView

app_name = ChecksConfig.name

router = DefaultRouter()
router.register(r'questions', QuestionViewSet, basename='questions')
router.register(r'answers', AnswerViewSet, basename='answers')


urlpatterns = [
    path('choices/create/', ChoiceCreateAPIView.as_view(), name='choice-create'),
    path('choices/', ChoiceListAPIView.as_view(), name='choice-list'),

] + router.urls
