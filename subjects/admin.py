from django import forms
from django.contrib import admin

from .models import Institute, Program, Subject, Chapter, TeacherAssignment


@admin.register(Institute)
class InstituteAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
    )

    list_filter = (
        "is_active",
    )


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "institute",
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "institute__name",
    )

    list_filter = (
        "institute",
        "is_active",
    )


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "program",
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "program__name",
        "program__institute__name",
    )

    list_filter = (
        "program",
        "is_active",
    )



class TeacherAssignmentAdminForm(forms.ModelForm):
    class Meta:
        model = TeacherAssignment
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["teacher"].queryset = (
            self.fields["teacher"].queryset.filter(
                user_type="TEACHER",
                is_active=True,
            )
        )


@admin.register(TeacherAssignment)
class TeacherAssignmentAdmin(admin.ModelAdmin):
    form = TeacherAssignmentAdminForm

    list_display = (
        "teacher",
        "subject",
        "is_active",
        "created_at",
    )

    search_fields = (
        "teacher__first_name",
        "teacher__last_name",
        "teacher__email",
        "teacher__mobile_number",
        "subject__name",
    )

    list_filter = (
        "subject",
        "is_active",
    )

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "subject",
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "subject__name",
        "subject__program__name",
    )

    list_filter = (
        "subject",
        "is_active",
    )