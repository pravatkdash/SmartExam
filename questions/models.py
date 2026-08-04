from django.db import models

from common.models import BaseModel
from subjects.models import Chapter


class Difficulty(models.TextChoices):
    EASY = "EASY", "Easy"
    MEDIUM = "MEDIUM", "Medium"
    HARD = "HARD", "Hard"


class Question(BaseModel):

    chapter = models.ForeignKey(
        Chapter,
        on_delete=models.PROTECT,
        related_name="questions",
    )

    question_text = models.TextField()

    explanation = models.TextField(
        blank=True,
    )

    difficulty = models.CharField(
        max_length=10,
        choices=Difficulty.choices,
        default=Difficulty.MEDIUM,
    )

    marks = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=1,
    )

    negative_marks = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
    )
    is_multiple_answer = models.BooleanField(
        default=False,
    )

    class Meta:
        ordering = [
            "chapter__subject__exam__name",
            "chapter__subject__name",
            "chapter__name",
        ]

    def __str__(self):
        return f"{self.chapter} | {self.question_text[:60]}"


class Option(BaseModel):

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="options",
    )

    option_text = models.TextField()

    is_correct = models.BooleanField(
        default=False,
    )

    display_order = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ["display_order"]
        constraints = [
            models.UniqueConstraint(
                fields=["question", "display_order"],
                name="unique_option_order_per_question",
            )
        ]

    def __str__(self):
        return f"Option {self.display_order} - {self.question}"