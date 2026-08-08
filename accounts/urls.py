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
]