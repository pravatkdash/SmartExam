from django.conf import settings
from django.db import models

from common.models import BaseModel
from questions.models import Question, Option


class AssessmentStatus(models.TextChoices):
    DRAFT = "DRAFT", "Draft"
    PUBLISHED = "PUBLISHED", "Published"


class Assessment(BaseModel):
    subject = models.ForeignKey(
        "subjects.Subject",
        on_delete=models.PROTECT,
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

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_assessments",
    )

    class Meta:
        ordering = [
            "subject",
            "name",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "created_by",
                    "subject",
                    "name",
                ],
                name="unique_assessment_name_per_teacher_per_subject",
            )
        ]

    def __str__(self):
        return f"{self.subject} → {self.name}"


class AssessmentQuestion(BaseModel):
    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE,
        related_name="assessment_questions",
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="assessment_questions",
    )

    display_order = models.PositiveIntegerField()

    class Meta:
        ordering = [
            "assessment",
            "display_order",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "assessment",
                    "question",
                ],
                name="unique_question_per_assessment",
            ),
            models.UniqueConstraint(
                fields=[
                    "assessment",
                    "display_order",
                ],
                name="unique_display_order_per_assessment",
            ),
        ]



class AssessmentAttemptStatus(models.TextChoices):
    IN_PROGRESS = "IN_PROGRESS", "In Progress"
    SUBMITTED = "SUBMITTED", "Submitted"
    EXPIRED = "EXPIRED", "Expired"


class AssessmentAttempt(BaseModel):

    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.PROTECT,
        related_name="attempts",
    )

    """
    Every AssessmentAttempt belongs to one User/student. 
    Multiple attempts can belong to the same student. 
    The student cannot be deleted while those attempts exist, 
    and we can access all of a student's attempts using student.assessment_attempts.
    """
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="assessment_attempts",
    )

    started_at = models.DateTimeField()

    expires_at = models.DateTimeField()

    submitted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=AssessmentAttemptStatus.choices,
        default=AssessmentAttemptStatus.IN_PROGRESS,
    )

    score = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
    )

    class Meta:
        """
         meaning descending oder sorting
        """

        ordering = [
            "-started_at",
        ]


    def __str__(self):
        return (
            f"{self.student} → "
            f"{self.assessment} → "
            f"{self.status}"
        )


class AttemptQuestion(BaseModel):

    attempt = models.ForeignKey(
        AssessmentAttempt,
        on_delete=models.CASCADE,
        related_name="attempt_questions",
    )

    question = models.ForeignKey(
        Question,
        on_delete=models.PROTECT,
        related_name="attempt_questions",
    )

    display_order = models.PositiveIntegerField()

    class Meta:
        ordering = [
            "display_order",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "attempt",
                    "question",
                ],
                name="unique_question_per_attempt",
            ),
            models.UniqueConstraint(
                fields=[
                    "attempt",
                    "display_order",
                ],
                name="unique_display_order_per_attempt",
            ),
        ]

    def __str__(self):
        return (
            f"{self.attempt} → "
            f"Question {self.display_order}"
        )


class StudentAnswer(BaseModel):

    attempt_question = models.OneToOneField(
        AttemptQuestion,
        on_delete=models.CASCADE,
        related_name="answer",
    )

    selected_options = models.ManyToManyField(
        Option,
        blank=True,
        related_name="student_answers",
    )

    answered_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = [
            "attempt_question__display_order",
        ]

    def __str__(self):
        return (
            f"{self.attempt_question} → "
            f"Student Answer"
        )

