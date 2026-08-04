from django import forms
from django.contrib import admin
from django.db import models

from .models import Question, Option
from .admin_forms import QuestionAdminForm, OptionInlineFormSet, OptionAdminForm


class OptionInline(admin.TabularInline):
    model = Option
    form = OptionAdminForm
    formset = OptionInlineFormSet

    extra = 4

    verbose_name = "Possible Answer"
    verbose_name_plural = "Possible Answers"

    exclude = (
        "display_order",
        "is_active",
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
    )

    formfield_overrides = {
        models.TextField: {
            "widget": forms.Textarea(
                attrs={
                    "rows": 4,
                    "cols": 100,
                }
            )
        }
    }


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    form = QuestionAdminForm

    list_display = (
        "chapter",
        "question_preview",
        "difficulty",
        "marks",
        "is_active",
    )

    @admin.display(description="Question")
    def question_preview(self, obj):
        return obj.question_text

    search_fields = (
        "question_text",
    )

    list_filter = (
        "difficulty",
        "chapter",
        "is_active",
    )

    fieldsets = (
        (
            "Question Information",
            {
                "fields": (
                    "chapter",
                    "question_text",
                    "explanation",
                )
            },
        ),
        (
            "Scoring",
            {
                "fields": (
                    "difficulty",
                    (
                        "marks",
                        "negative_marks",
                    ),
                )
            },
        ),
        (
            "Settings",
            {
                "fields": (
                    "is_multiple_answer",
                )
            },
        ),
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    inlines = [
        OptionInline,
    ]

    def get_fieldsets(self, request, obj=None):
        """
        Show audit information only while editing.
        """
        fieldsets = list(super().get_fieldsets(request, obj))

        if obj:
            fieldsets.append(
                (
                    "Audit Information",
                    {
                        "fields": (
                            "created_at",
                            "updated_at",
                        )
                    },
                )
            )

        return fieldsets

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)

        for obj in formset.deleted_objects:
            obj.delete()

        order = 1

        for instance in instances:
            instance.display_order = order
            instance.save()
            order += 1

        formset.save_m2m()


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):

    list_display = (
        "question",
        "display_order",
        "option_text",
        "is_correct",
    )