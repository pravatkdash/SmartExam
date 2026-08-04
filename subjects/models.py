import uuid

from django.db import models
from common.models import BaseModel


class Exam(BaseModel):

    name = models.CharField(
        max_length=100,
        unique=True,
    )

    description = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Exam"
        verbose_name_plural = "Exams"

    def __str__(self):
        return self.name


class Subject(BaseModel):

    exam = models.ForeignKey(
        Exam,
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
                fields=["exam", "name"],
                name="unique_subject_per_exam",
            )
        ]
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"

    def __str__(self):
        return f"{self.exam.name} - {self.name}"


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