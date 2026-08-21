from django import forms
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