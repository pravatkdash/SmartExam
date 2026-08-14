from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
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


    fieldsets = UserAdmin.fieldsets + (
        (
            "SmartExam Information",
            {
                "fields": (
                    "mobile_number",
                    "mobile_verified",
                    "user_type",
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
                )
            },
        ),
    )