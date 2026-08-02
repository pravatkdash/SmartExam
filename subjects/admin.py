from django.contrib import admin

from .models import Exam, Subject, Chapter


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "is_active",
        "created_at",
    )

    search_fields = ("name",)

    list_filter = ("is_active",)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "exam",
        "is_active",
    )

    search_fields = (
        "name",
    )

    list_filter = (
        "exam",
        "is_active",
    )


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "subject",
        "is_active",
    )

    search_fields = (
        "name",
    )

    list_filter = (
        "subject",
        "is_active",
    )