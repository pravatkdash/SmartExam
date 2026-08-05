from django.conf import settings
from django.db import models

from common.models import BaseModel
from subjects.models import Exam


class AssessmentStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    PUBLISHED = "PUBLISHED", "Published"

class Assessment(BaseModel):
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name="assessments",
    )

    name = models.CharField(
        max_length=100,
        db_index=True,
    )

    description = models.TextField(
        blank=True,
    )

    duration_minutes = models.PositiveIntegerField()

    status = models.CharField(
        max_length=20,
        choices=AssessmentStatus.choices,
        default=AssessmentStatus.DRAFT,
    )

    is_active = models.BooleanField(
        default=False,
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_assessments",
    )

    class Meta:
        ordering = [
            "exam",
            "name",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "created_by",
                    "exam",
                    "name",
                ],
                name="unique_assessment_name_per_teacher_per_exam",
            )
        ]

    def __str__(self):
        return f"{self.exam} → {self.name}"