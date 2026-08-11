from django.urls import path
from . import views

urlpatterns = [

    path(
        "<uuid:attempt_id>/exam/<int:question_number>/",
        views.assessment_exam_view,
        name="assessment_exam",
    ),

    path(
        "<uuid:attempt_id>/result/",
        views.assessment_result_view,
        name="assessment_result",
    ),

    path(
        "start/<uuid:assessment_id>/",
        views.start_assessment_view,
        name="start_assessment",
    ),
]