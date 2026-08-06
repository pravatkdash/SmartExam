from django.contrib import admin

from assessment.models import Assessment
from .admin_forms import AssessmentAdminForm


# Register your models here.


@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    form = AssessmentAdminForm

    list_display = (
        "exam",
        "assessment_name",
        "duration",
        "status",
        "is_active",
    )


    search_fields = (
        "name",
        "exam__name",
    )

    list_filter = (
        "exam",
        "status",
        "is_active",
    )

    fieldsets = (
        (
            "Assessment Information",
            {
                "fields": (
                    "exam",
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

    exclude = (
        "created_by",
    )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user

        super().save_model(request, obj, form, change)

    @admin.display(description="Assessment", ordering="name",)
    def assessment_name(self, obj):
        return obj.name

    @admin.display(description="Duration", ordering="duration_minutes",
)
    def duration(self, obj):
        return f"{obj.duration_minutes} min"