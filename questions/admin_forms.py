from django import forms
from django.forms import BaseInlineFormSet
from django.core.exceptions import ValidationError

from .models import Question, Option

class OptionAdminForm(forms.ModelForm):

    class Meta:
        model = Option
        fields = "__all__"

        widgets = {
            "option_text": forms.TextInput(
                attrs={
                    "style": "width:600px;",
                }
            )
        }


class QuestionAdminForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = "__all__"

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
                    "rows": 2,
                    "style": "width:600px;",
                }
            ),
            "explanation": forms.Textarea(
                attrs={
                    "rows": 2,
                    "style": "width:600px;",
                }
            ),
        }



class OptionInlineFormSet(BaseInlineFormSet):

    def clean(self):
        super().clean()

        correct_answers = 0

        for form in self.forms:

            print("Cleaned Data:", form.cleaned_data)

            if not hasattr(form, "cleaned_data"):
                continue

            if form.cleaned_data.get("DELETE", False):
                continue

            if not form.cleaned_data:
                continue

            if form.cleaned_data.get("is_correct"):
                correct_answers += 1

        question = self.instance

        if question.is_multiple_answer:

            if correct_answers == 0:
                raise ValidationError(
                    "Multiple answer questions must have at least one correct option."
                )

        else:

            if correct_answers != 1:
                raise ValidationError(
                    "Single answer questions must have exactly one correct option."
                )