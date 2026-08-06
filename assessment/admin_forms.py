from django import forms

from .models import Assessment, AssessmentStatus


class AssessmentAdminForm(forms.ModelForm):

    class Meta:
        model = Assessment
        fields = "__all__"

        widgets = {
            "description": forms.Textarea(
                attrs={
                    "rows": 2,
                    "style": "width:600px;",
                }
            ),
        }

    # cleaned_data looks like:
    # {
    #     "exam": <Exam: NEET>,
    #     "name": "Biology Mock Test 1",
    #     "description": "",
    #     "duration_minutes": 60,
    #     "status": "DRAFT",
    #     "is_active": True,
    # }

    def clean(self):
        cleaned_data = super().clean()

        status = cleaned_data.get("status")
        is_active = cleaned_data.get("is_active")

        if status == AssessmentStatus.DRAFT and is_active:
            raise forms.ValidationError(
                "An assessment must be published before it can be made active."
            )

        return cleaned_data