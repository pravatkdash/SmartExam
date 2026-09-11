from django import forms
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet, inlineformset_factory

from .models import Question, Option


class TeacherQuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = (
            "question_text",
            "explanation",
            "difficulty",
            "marks",
            "negative_marks",
            "is_multiple_answer",
        )

        labels = {
            "question_text": "Question",
            "is_multiple_answer": "Allow Multiple Correct Answers",
        }

        help_texts = {
            "negative_marks": "Penalty deducted for an incorrect answer.",
        }

        widgets = {
            "question_text": forms.Textarea(
                attrs={
                    "rows": 4,
                    "style": "width:600px;",
                }
            ),
            "explanation": forms.Textarea(
                attrs={
                    "rows": 3,
                    "style": "width:600px;",
                }
            ),
        }


class TeacherOptionForm(forms.ModelForm):

    class Meta:
        model = Option
        fields = (
            "option_text",
            "is_correct",
        )

        widgets = {
            "option_text": forms.TextInput(
                attrs={
                    "style": "width:600px;",
                }
            )
        }

class TeacherOptionBaseFormSet(BaseInlineFormSet):

    """
    Save options while automatically maintaining display_order.

    The order of the forms in the formset determines the
    display_order of the options.
    """

    def clean(self):
        super().clean()

        if any(self.errors):
            return

        correct_answers = 0

        for form in self.forms:

            if not form.cleaned_data:
                continue

            if form.cleaned_data.get("DELETE", False):
                continue

            # Ignore completely empty option forms
            if not form.cleaned_data.get("option_text"):
                continue

            if form.cleaned_data.get("is_correct", False):
                correct_answers += 1

        # Get is_multiple_answer from the temporary Question instance
        is_multiple_answer = getattr(
            self.instance,
            "is_multiple_answer",
            False,
        )

        # At least one correct answer is always required
        if correct_answers == 0:
            raise ValidationError(
                "Please select at least one correct option."
            )

        # Single-answer question must have exactly one
        if not is_multiple_answer and correct_answers > 1:
            raise ValidationError(
                "Single-answer questions must have exactly one correct option."
            )

    def save(self, commit=True):

        instances = super().save(commit=False)

        display_order = 1

        for instance in instances:

            if not instance.option_text:
                continue

            instance.display_order = display_order
            display_order += 1

            if commit:
                instance.save()

        return instances



TeacherOptionFormSet = inlineformset_factory(
    Question,
    Option,
    form=TeacherOptionForm,
    formset=TeacherOptionBaseFormSet,
    extra=0,
    can_delete=False,
)


TeacherOptionAddFormSet = inlineformset_factory(
    Question,
    Option,
    form=TeacherOptionForm,
    formset=TeacherOptionBaseFormSet,
    extra=4,
    can_delete=False,
)