from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from common.models import BaseModel


class Institute(BaseModel):
    name = models.CharField(
        max_length=200,
        unique=True,
    )
    description = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Institute"
        verbose_name_plural = "Institutes"

    def __str__(self):
        return self.name


class Program(BaseModel):
    institute = models.ForeignKey(
        Institute,
        on_delete=models.PROTECT,
        related_name="programs",
    )
    name = models.CharField(
        max_length=200,
    )
    description = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["institute", "name"],
                name="unique_program_per_institute",
            )
        ]
        verbose_name = "Program"
        verbose_name_plural = "Programs"

    def __str__(self):
        return f"{self.institute.name} - {self.name}"


class Subject(BaseModel):
    program = models.ForeignKey(
        Program,
        on_delete=models.PROTECT,
        related_name="subjects",
    )
    name = models.CharField(
        max_length=100,
    )
    description = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["program", "name"],
                name="unique_subject_per_program",
            )
        ]
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"

    def __str__(self):
        return f"{self.program.name} - {self.name}"


class TeacherAssignment(BaseModel):
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="teacher_assignments",
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT,
        related_name="teacher_assignments",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["teacher", "subject"],
                name="unique_teacher_assignment_per_subject",
            )
        ]
        verbose_name = "Teacher Assignment"
        verbose_name_plural = "Teacher Assignments"

    def clean(self):
        if self.teacher and self.teacher.user_type != "TEACHER":
            raise ValidationError(
                "Only users with the Teacher role can be assigned to a subject."
            )

    def __str__(self):
        return f"{self.teacher} → {self.subject}"


class Chapter(BaseModel):
    subject = models.ForeignKey(
        Subject,
        on_delete=models.PROTECT,
        related_name="chapters",
    )
    name = models.CharField(
        max_length=150,
    )
    description = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                fields=["subject", "name"],
                name="unique_chapter_per_subject",
            )
        ]
        verbose_name = "Chapter"
        verbose_name_plural = "Chapters"

    def __str__(self):
        return f"{self.subject.name} → {self.name}"