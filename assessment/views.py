from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from assessment.models import Assessment, AssessmentAttempt, StudentAnswer, AssessmentAttemptStatus
from assessment.services.attempt_service import start_assessment
from assessment.services.result_service import submit_assessment


@login_required
def assessment_exam_view(request, attempt_id, question_number):
    attempt = get_object_or_404(
        AssessmentAttempt,
        id=attempt_id,
        student=request.user,
    )

    # -------------------------------------------------
    # 1. Submitted attempt → go directly to result
    # -------------------------------------------------
    if attempt.status == AssessmentAttemptStatus.SUBMITTED:
        return redirect(
            "assessment_result",
            attempt_id=attempt.id,
        )

    # -------------------------------------------------
    # 2. Load attempt questions
    # -------------------------------------------------
    attempt_questions = (
        attempt.attempt_questions
        .select_related("question")
        .prefetch_related(
            "question__options",
        )
        .order_by("display_order")
    )

    total_questions = attempt_questions.count()

    # -------------------------------------------------
    # 3. Validate question number
    # -------------------------------------------------
    if question_number < 1 or question_number > total_questions:
        return redirect(
            "assessment_exam",
            attempt_id=attempt.id,
            question_number=1,
        )

    attempt_question = attempt_questions[question_number - 1]

    student_answer = get_object_or_404(
        StudentAnswer,
        attempt_question=attempt_question,
    )

    # -------------------------------------------------
    # 4. Handle POST
    # -------------------------------------------------
    if request.method == "POST":

        navigation = request.POST.get("navigation")

        # ---------------------------------------------
        # Submit Exam
        # ---------------------------------------------
        if navigation == "submit":

            submit_assessment(attempt)

            return redirect(
                "assessment_result",
                attempt_id=attempt.id,
            )

        # ---------------------------------------------
        # Save answer
        # ---------------------------------------------
        option_ids = request.POST.getlist("answers")

        options = attempt_question.question.options.filter(
            id__in=option_ids
        )

        student_answer.selected_options.set(options)

        student_answer.answered_at = timezone.now()

        student_answer.save(
            update_fields=[
                "answered_at",
            ]
        )

        # ---------------------------------------------
        # Next question
        # ---------------------------------------------
        if navigation == "next":
            return redirect(
                "assessment_exam",
                attempt_id=attempt.id,
                question_number=question_number + 1,
            )

        # ---------------------------------------------
        # Previous question
        # ---------------------------------------------
        if navigation == "previous":
            return redirect(
                "assessment_exam",
                attempt_id=attempt.id,
                question_number=question_number - 1,
            )

        # ---------------------------------------------
        # Stay on current question
        # ---------------------------------------------
        return redirect(
            "assessment_exam",
            attempt_id=attempt.id,
            question_number=question_number,
        )

    # -------------------------------------------------
    # 5. Display question
    # -------------------------------------------------
    options = attempt_question.question.options.all()

    return render(
        request,
        "assessment/exam.html",
        {
            "attempt": attempt,
            "attempt_question": attempt_question,
            "options": options,
            "student_answer": student_answer,
            "question_number": question_number,
            "total_questions": total_questions,
        },
    )


@login_required
def assessment_result_view(request, attempt_id):
    attempt = get_object_or_404(
        AssessmentAttempt,
        id=attempt_id,
        student=request.user,
    )

    return render(
        request,
        "assessment/result.html",
        {
            "attempt": attempt,
        },
    )


@login_required
def start_assessment_view(request, assessment_id):

    assessment = get_object_or_404(
        Assessment,
        id=assessment_id,
        status="PUBLISHED",
        is_active=True,
    )

    attempt = start_assessment(
        student=request.user,
        assessment=assessment,
    )

    return redirect(
        "assessment_exam",
        attempt_id=attempt.id,
        question_number=1,
    )