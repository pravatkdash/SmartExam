from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from assessment.models import (
    AssessmentAttempt,
    AssessmentAttemptStatus,
    AssessmentStatus,
    AttemptQuestion,
    StudentAnswer,
)


@transaction.atomic
def start_assessment(student, assessment):
    """
    Create a new assessment attempt for a student.
    """

    # 1. Assessment must be published
    if assessment.status != AssessmentStatus.PUBLISHED:
        raise ValueError(
            "Only published assessments can be started."
        )

    # 2. Assessment must be active
    if not assessment.is_active:
        raise ValueError(
            "This assessment is not currently active."
        )

    # 3. Return existing in-progress attempt
    existing_attempt = (
        AssessmentAttempt.objects
        .filter(
            assessment=assessment,
            student=student,
            status=AssessmentAttemptStatus.IN_PROGRESS,
        )
        .first()
    )

    if existing_attempt:
        return existing_attempt

    # 4. Start time
    started_at = timezone.now()

    # 5. Calculate expiry time
    expires_at = (
        started_at
        + timedelta(
            minutes=assessment.duration_minutes
        )
    )

    # 6. Create the attempt
    attempt = AssessmentAttempt.objects.create(
        assessment=assessment,
        student=student,
        started_at=started_at,
        expires_at=expires_at,
        status=AssessmentAttemptStatus.IN_PROGRESS,
    )

    # 7. Get questions from the assessment
    assessment_questions = (
        assessment.assessment_questions
        .select_related("question")
        .order_by("display_order")
    )

    # 8. Create AttemptQuestion + StudentAnswer
    for assessment_question in assessment_questions:

        attempt_question = AttemptQuestion.objects.create(
            attempt=attempt,
            question=assessment_question.question,
            display_order=assessment_question.display_order,
        )

        StudentAnswer.objects.create(
            attempt_question=attempt_question,
            answered_at=None,
        )

    return attempt