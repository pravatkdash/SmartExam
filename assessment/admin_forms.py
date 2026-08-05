from django import forms

from .models import Assessment


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