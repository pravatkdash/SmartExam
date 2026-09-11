from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserAdminForm
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    form = UserAdminForm

    ordering = ("email",)

    list_display = (
        "email",
        "first_name",
        "last_name",
        "user_type",
        "mobile_verified",
        "is_staff",
        "is_active",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        (
            "Personal Information",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "mobile_number",
                )
            },
        ),
        (
            "SmartExam Information",
            {
                "fields": (
                    "user_type",
                    "institute",
                    "mobile_verified",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Important Dates",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "mobile_number",
                    "first_name",
                    "last_name",
                    "user_type",
                    "institute",
                )
            },
        ),
    )