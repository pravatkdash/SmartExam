from django.db import transaction
from django.utils import timezone

from assessment.models import (
    AssessmentAttempt,
    AssessmentAttemptStatus,
)


@transaction.atomic
def submit_assessment(attempt):
    """
    Submit an assessment attempt and calculate the score.

    V1 scoring:
    - Correct answer  -> full marks
    - Wrong answer    -> 0
    - Unanswered      -> 0
    - No negative marking
    """

    # 1. Attempt must be in progress
    if attempt.status != AssessmentAttemptStatus.IN_PROGRESS:
        raise ValueError(
            "This assessment attempt cannot be submitted."
        )

    # 2. Get all questions in this attempt
    attempt_questions = (
        attempt.attempt_questions
        .select_related("question")
        .prefetch_related(
            "question__options",
            "answer__selected_options",
        )
        .order_by("display_order")
    )

    total_score = 0

    # 3. Evaluate every question
    for attempt_question in attempt_questions:

        question = attempt_question.question

        student_answer = getattr(
            attempt_question,
            "answer",
            None,
        )

        # No StudentAnswer record
        if not student_answer:
            continue

        selected_options = set(
            student_answer.selected_options.all()
        )

        # Student did not answer
        if not selected_options:
            continue

        correct_options = set(
            question.options.filter(
                is_correct=True
            )
        )

        # Exact match required
        if selected_options == correct_options:
            total_score += question.marks

    # 4. Save result
    attempt.score = total_score
    attempt.status = AssessmentAttemptStatus.SUBMITTED
    attempt.submitted_at = timezone.now()

    attempt.save(
        update_fields=[
            "score",
            "status",
            "submitted_at",
        ]
    )

    return attempt