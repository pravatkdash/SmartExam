from django.urls import path

from . import views


urlpatterns = [
    path(
        "dashboard/",
        views.dashboard,
        name="institute_dashboard",
    ),

    path(
        "teachers/",
        views.teacher_list,
        name="institute_teacher_list",
    ),

    path(
        "teachers/add/",
        views.teacher_create,
        name="institute_teacher_create",
    ),

    path(
        "teachers/<uuid:teacher_id>/assignments/",
        views.teacher_assignment,
        name="institute_teacher_assignment",
    ),

    path(
        "students/",
        views.student_list,
        name="institute_student_list",
    ),

    path(
        "students/add/",
        views.student_create,
        name="institute_student_create",
    ),
]