from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.student_register, name="student_register"),
    path("register/verify-otp/", views.student_verify_otp, name="student_verify_otp",),
    path("register/details/", views.student_registration_details, name="student_registration_details",),
    path("register/success/", views.student_registration_success, name="student_registration_success",),
    path("login/", views.student_login, name="student_login",),
    path("student/dashboard/", views.student_dashboard, name="student_dashboard",),
    path("logout/", views.student_logout, name="student_logout",),
    path(
        "teacher/login/",
        views.teacher_login,
        name="teacher_login",
    ),
    path(
        "teacher/",
        views.teacher_dashboard,
        name="teacher_dashboard",
    ),
    path(
        "subjects/<uuid:subject_id>/",
        views.teacher_subject_chapters,
        name="teacher_subject_chapters",
    ),

    path(
        "teacher/<uuid:subject_id>/chapters/",
        views.teacher_subject_chapters,
        name="teacher_subject_chapters",
    ),

    path(
        "teacher/<uuid:subject_id>/chapter/<uuid:chapter_id>/questions/add/",
        views.teacher_add_question,
        name="teacher_add_question",
    ),

    path(
        "teacher/<uuid:subject_id>/chapter/<uuid:chapter_id>/questions/<uuid:question_id>/edit/",
        views.teacher_edit_question,
        name="teacher_edit_question",
    ),

    path(
        "teacher/<uuid:subject_id>/chapter/<uuid:chapter_id>/questions/<uuid:question_id>/delete/",
        views.teacher_delete_question,
        name="teacher_delete_question",
    ),

    path(
        "teacher/<uuid:subject_id>/chapter/<uuid:chapter_id>/questions/",
        views.teacher_chapter_questions,
        name="teacher_chapter_questions",
    ),

    path(
        "teacher/<uuid:subject_id>/chapter/<uuid:chapter_id>/questions/<uuid:question_id>/",
        views.teacher_question_detail,
        name="teacher_question_detail",
    ),

# path(
#     "institute-admin/login/",
#     views.institute_admin_login,
#     name="institute_admin_login",
# ),

# path(
#     "institute-admin/",
#     views.institute_admin_dashboard,
#     name="institute_admin_dashboard",
# ),

    path(
        "institute/login/",
        views.institute_admin_login,
        name="institute_admin_login",
    ),


]