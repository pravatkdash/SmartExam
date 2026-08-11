from .models import Question
from assessment.models import AssessmentStatus


def is_question_locked(question):
    """
    A question is locked if it is used by any published assessment.
    """

    return question.assessment_questions.filter(
        assessment__status=AssessmentStatus.PUBLISHED
    ).exists()


def get_question_lock_message(question):
    assessments = question.assessment_questions.filter(
        assessment__status=AssessmentStatus.PUBLISHED
    ).select_related("assessment")

    names = ", ".join(
        assessment.assessment.name
        for assessment in assessments
    )

    return (
        f"This question cannot be modified because it is used "
        f"in published assessment(s): {names}."
    )