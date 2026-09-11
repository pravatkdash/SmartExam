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

        if any(self.errors):
            return

        correct_answers = 0

        for form in self.forms:

            if not form.cleaned_data:
                continue

            if form.cleaned_data.get("DELETE", False):
                continue

            if form.cleaned_data.get("is_correct", False):
                correct_answers += 1

        # At least one correct answer is always required
        if correct_answers == 0:
            raise ValidationError(
                "Please select at least one correct option."
            )

        # For single-answer questions, exactly one is required
        question = self.instance

        if not question.is_multiple_answer and correct_answers > 1:
            raise ValidationError(
                "Single-answer questions must have exactly one correct option."
            )