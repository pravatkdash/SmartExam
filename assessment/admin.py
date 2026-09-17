from django.contrib import admin

from assessment.models import Assessment, AssessmentQuestion
from .admin_forms import AssessmentAdminForm, AssessmentQuestionInlineFormSet


# Register your models here.

class AssessmentQuestionInline(admin.TabularInline):
    model = AssessmentQuestion
    formset = AssessmentQuestionInlineFormSet

    exclude = (
        "is_active",
        "display_order",
    )


@admin.register(AssessmentQuestion)
class AssessmentQuestionAdmin(admin.ModelAdmin):
    list_display = (
        "assessment",
        "display_order",
        "question",
    )


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    form = AssessmentAdminForm

    list_display = (
        "program",
        "name",
        "duration_minutes",
        "status",
        "created_by",
    )

    list_filter = (
        "program",
        "status",
    )

    search_fields = (
        "name",
        "program__name",
    )

    fieldsets = (
        (
            "Assessment Information",
            {
                "fields": (
                    "program",
                    "name",
                    "description",
                ),
            },
        ),
        (
            "Configuration",
            {
                "fields": (
                    "duration_minutes",
                    "status",
                    "is_active",
                ),
            },
        ),
    )

    inlines = [
        AssessmentQuestionInline,
    ]

    exclude = (
        "created_by",
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user

        super().save_model(request, obj, form, change)

    @admin.display(
        description="Assessment",
        ordering="name",
    )
    def assessment_name(self, obj):
        return obj.name

    @admin.display(
        description="Duration",
        ordering="duration_minutes",
    )
    def duration(self, obj):
        return f"{obj.duration_minutes} min"