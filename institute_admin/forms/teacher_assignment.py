from django import forms

from subjects.models import Subject, Chapter, TeacherAssignment


class TeacherAssignmentForm(forms.ModelForm):

    ASSIGNMENT_TYPE_CHOICES = (
        ("subject", "Subject"),
        ("chapter", "Chapter"),
    )

    assignment_type = forms.ChoiceField(
        choices=ASSIGNMENT_TYPE_CHOICES,
        widget=forms.RadioSelect,
    )

    class Meta:
        model = TeacherAssignment
        fields = (
            "assignment_type",
            "subject",
            "chapter",
        )

    def __init__(self, *args, institute=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.institute = institute

        self.fields["subject"].queryset = (
            Subject.objects
            .filter(
                program__institute=institute,
                is_active=True,
            )
            .order_by("name")
        )

        self.fields["chapter"].queryset = (
            Chapter.objects
            .filter(
                subject__program__institute=institute,
                subject__is_active=True,
            )
            .order_by(
                "subject__name",
                "name",
            )
        )

    def clean(self):
        cleaned_data = super().clean()

        assignment_type = cleaned_data.get("assignment_type")
        subject = cleaned_data.get("subject")
        chapter = cleaned_data.get("chapter")

        if assignment_type == "subject":

            if not subject:
                self.add_error(
                    "subject",
                    "Please select a subject.",
                )

            if chapter:
                self.add_error(
                    "chapter",
                    "Chapter should not be selected for a subject assignment.",
                )

        elif assignment_type == "chapter":

            if not chapter:
                self.add_error(
                    "chapter",
                    "Please select a chapter.",
                )

            if subject:
                self.add_error(
                    "subject",
                    "Subject should not be selected for a chapter assignment.",
                )

        return cleaned_data

    def save(self, commit=True):
        assignment = super().save(commit=False)

        assignment.teacher = self.instance.teacher

        if self.cleaned_data["assignment_type"] == "subject":
            assignment.subject = self.cleaned_data["subject"]
            assignment.chapter = None

        else:
            assignment.subject = None
            assignment.chapter = self.cleaned_data["chapter"]

        if commit:
            assignment.save()

        return assignment