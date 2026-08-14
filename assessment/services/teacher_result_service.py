from django.db.models import Count, Max

from assessment.models import AssessmentAttempt
from accounts.models import UserType


def get_assessment_results(assessment):
    return (
        AssessmentAttempt.objects
        .filter(
            assessment=assessment,
            status="SUBMITTED",
        )
        .values(
            "student_id",
            "student__first_name",
            "student__last_name",
        )
        .annotate(
            attempt_count=Count("id"),
            latest_score=Max("score"),
        )
        .order_by(
            "student__first_name",
            "student__last_name",
        )
    )