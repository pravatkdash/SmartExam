from django.urls import path

from . import views


urlpatterns = [
    path(
        "institute-admin/programs/",
        views.institute_program_list,
        name="institute_program_list",
    ),
    path(
        "institute-admin/programs/create/",
        views.institute_program_create,
        name="institute_program_create",
    ),

    path(
        "institute-admin/programs/<uuid:program_id>/subjects/",
        views.institute_program_subject_list,
        name="institute_program_subject_list",
    ),

    path(
        "institute-admin/programs/<uuid:program_id>/subjects/create/",
        views.institute_subject_create,
        name="institute_subject_create",
    ),

    path(
        "institute/program/<uuid:program_id>/subject/<uuid:subject_id>/chapters/",
        views.institute_subject_chapter_list,
        name="institute_subject_chapter_list",
    ),

    path(
        "institute/program/<uuid:program_id>/subject/<uuid:subject_id>/chapters/add/",
        views.institute_subject_chapter_create,
        name="institute_subject_chapter_create",
    ),

    path(
        "institute/dashboard/",
        views.institute_dashboard,
        name="institute_dashboard",
    ),
]