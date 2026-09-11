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

    path(
        "teacher/",
        views.teacher_assessment_list,
        name="teacher_assessment_list",
    ),

    path(
        "teacher/create/",
        views.teacher_assessment_create,
        name="teacher_assessment_create",
    ),

    path(
        "teacher/<uuid:assessment_id>/",
        views.teacher_assessment_detail,
        name="teacher_assessment_detail",
    ),

    path(
        "teacher/<uuid:assessment_id>/questions/add/",
        views.teacher_assessment_add_questions,
        name="teacher_assessment_add_questions",
    ),

    path(
        "teacher/<uuid:assessment_id>/publish/",
        views.teacher_assessment_publish,
        name="teacher_assessment_publish",
    ),


]