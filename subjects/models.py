from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from accounts.models import UserType
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
        blank=True,
        null=True,
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
        if self.institute:
            return f"{self.institute.name} - {self.name}"

        return f"SmartExam - {self.name}"


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
        blank=True,
        null=True,
    )

    chapter = models.ForeignKey(
        Chapter,
        on_delete=models.PROTECT,
        related_name="teacher_assignments",
        blank=True,
        null=True,
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(subject__isnull=False)
                    & models.Q(chapter__isnull=True)
                )
                | (
                    models.Q(subject__isnull=True)
                    & models.Q(chapter__isnull=False)
                ),
                name="teacher_assignment_subject_or_chapter",
            ),
            models.UniqueConstraint(
                fields=["teacher", "subject"],
                condition=models.Q(subject__isnull=False),
                name="unique_teacher_subject_assignment",
            ),
            models.UniqueConstraint(
                fields=["teacher", "chapter"],
                condition=models.Q(chapter__isnull=False),
                name="unique_teacher_chapter_assignment",
            ),
        ]

    def clean(self):
        if self.teacher and self.teacher.user_type != UserType.TEACHER:
            raise ValidationError(
                "Only users with the Teacher role can be assigned."
            )

        if self.subject and self.chapter:
            raise ValidationError(
                "Assignment cannot contain both subject and chapter."
            )

        if not self.subject and not self.chapter:
            raise ValidationError(
                "Assignment must contain either a subject or a chapter."
            )

        if self.chapter and self.subject:
            raise ValidationError(
                "Chapter already belongs to a subject."
            )

    def __str__(self):
        if self.subject:
            return f"{self.teacher} → {self.subject}"

        return f"{self.teacher} → {self.chapter}"



class StudentProgramEnrollment(BaseModel):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="program_enrollments",
    )
    program = models.ForeignKey(
        Program,
        on_delete=models.PROTECT,
        related_name="student_enrollments",
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "program"],
                name="unique_student_program_enrollment",
            )
        ]

    def __str__(self):
        return f"{self.student} - {self.program}"