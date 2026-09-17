from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from accounts.models import UserType
from assessment.models import Assessment, AssessmentAttempt, StudentAnswer, AssessmentAttemptStatus, AssessmentStatus, \
    AssessmentQuestion
from assessment.services.attempt_service import start_assessment
from assessment.services.result_service import submit_assessment
from questions.models import Question
from subjects.models import TeacherAssignment


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
        .select_related(
            "question",
            "answer",
        )
        .prefetch_related(
            "question__options",
        )
        .order_by(
            "display_order",
        )
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

    # -------------------------------------------------
    # 4. Current question
    # -------------------------------------------------

    attempt_question = attempt_questions[
        question_number - 1
    ]

    student_answer = get_object_or_404(
        StudentAnswer,
        attempt_question=attempt_question,
    )

    # -------------------------------------------------
    # 5. Handle POST
    # -------------------------------------------------

    if request.method == "POST":

        navigation = request.POST.get(
            "navigation"
        )

        # ---------------------------------------------
        # Save current answer
        # ---------------------------------------------

        option_ids = request.POST.getlist(
            "answers"
        )

        options = attempt_question.question.options.filter(
            id__in=option_ids
        )

        student_answer.selected_options.set(
            options
        )

        # ---------------------------------------------
        # Mark answered only if an option is selected
        # ---------------------------------------------

        if options.exists():

            student_answer.answered_at = timezone.now()

        else:

            student_answer.answered_at = None

        student_answer.save(
            update_fields=[
                "answered_at",
            ]
        )

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
        # Jump to question
        # ---------------------------------------------

        if navigation == "jump":

            target_question = request.POST.get(
                "target_question"
            )

            try:

                target_question = int(
                    target_question
                )

            except (
                TypeError,
                ValueError,
            ):

                target_question = question_number

            # -----------------------------------------
            # Validate target question
            # -----------------------------------------

            if (
                1 <= target_question <= total_questions
            ):

                return redirect(
                    "assessment_exam",
                    attempt_id=attempt.id,
                    question_number=target_question,
                )

            return redirect(
                "assessment_exam",
                attempt_id=attempt.id,
                question_number=question_number,
            )

        # ---------------------------------------------
        # Next question
        # ---------------------------------------------

        if navigation == "next":

            if question_number < total_questions:

                return redirect(
                    "assessment_exam",
                    attempt_id=attempt.id,
                    question_number=question_number + 1,
                )

            return redirect(
                "assessment_exam",
                attempt_id=attempt.id,
                question_number=question_number,
            )

        # ---------------------------------------------
        # Previous question
        # ---------------------------------------------

        if navigation == "previous":

            if question_number > 1:

                return redirect(
                    "assessment_exam",
                    attempt_id=attempt.id,
                    question_number=question_number - 1,
                )

            return redirect(
                "assessment_exam",
                attempt_id=attempt.id,
                question_number=question_number,
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
    # 6. Display question
    # -------------------------------------------------

    options = attempt_question.question.options.all()

    # -------------------------------------------------
    # 7. Question Navigator
    # -------------------------------------------------

    navigator_questions = list(
        attempt_questions
    )

    for navigator_question in navigator_questions:

        try:

            navigator_question.is_answered = (
                navigator_question.answer.answered_at
                is not None
            )

        except StudentAnswer.DoesNotExist:

            navigator_question.is_answered = False

    # -------------------------------------------------
    # 8. Render
    # -------------------------------------------------

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
            "navigator_questions": navigator_questions,
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


@login_required
def teacher_assessment_list(request):

    if request.user.user_type != UserType.TEACHER:
        return redirect("admin:index")

    assessments = (
        Assessment.objects
        .filter(
            created_by=request.user,
        )
        .select_related(
            "program",
            "program__institute",
        )
        .order_by(
            "-created_at",
        )
    )

    return render(
        request,
        "assessment/teacher_assessment_list.html",
        {
            "assessments": assessments,
        },
    )


@login_required
def teacher_assessment_create(request):

    if request.user.user_type != UserType.TEACHER:
        return redirect("admin:index")

    assignments = (
        TeacherAssignment.objects
        .filter(
            teacher=request.user,
            is_active=True,
            subject__is_active=True,
        )
        .select_related(
            "subject",
            "subject__program",
        )
        .order_by(
            "subject__name",
        )
    )

    if request.method == "POST":

        subject_id = request.POST.get("subject")
        name = request.POST.get("name", "").strip()
        description = request.POST.get("description", "").strip()
        duration_minutes = request.POST.get("duration_minutes")

        # ---------------------------------------------
        # Validate subject assignment
        # ---------------------------------------------

        assignment = get_object_or_404(
            TeacherAssignment.objects.select_related(
                "subject",
                "subject__program",
            ),
            teacher=request.user,
            subject_id=subject_id,
            is_active=True,
            subject__is_active=True,
        )

        subject = assignment.subject
        program = subject.program

        # ---------------------------------------------
        # Basic validation
        # ---------------------------------------------

        errors = []

        if not name:
            errors.append("Assessment name is required.")

        if not duration_minutes:
            errors.append("Duration is required.")
        else:
            try:
                duration_minutes = int(duration_minutes)

                if duration_minutes <= 0:
                    errors.append(
                        "Duration must be greater than zero."
                    )

            except ValueError:
                errors.append(
                    "Duration must be a valid number."
                )

        # ---------------------------------------------
        # Duplicate assessment name
        # ---------------------------------------------

        if not errors:

            if Assessment.objects.filter(
                created_by=request.user,
                program=program,
                name=name,
            ).exists():

                errors.append(
                    "You already have an assessment with this name "
                    "for this program."
                )

        # ---------------------------------------------
        # Validation failed
        # ---------------------------------------------

        if errors:

            for error in errors:
                messages.error(request, error)

        else:

            # -----------------------------------------
            # Create Draft Assessment
            # -----------------------------------------

            assessment = Assessment.objects.create(
                program=program,
                name=name,
                description=description,
                duration_minutes=duration_minutes,
                status=AssessmentStatus.DRAFT,
                is_active=False,
                created_by=request.user,
            )

            messages.success(
                request,
                "Assessment created successfully.",
            )

            return redirect(
                "teacher_assessment_list",
            )

    return render(
        request,
        "assessment/teacher_assessment_create.html",
        {
            "assignments": assignments,
        },
    )

'''Teacher A should never be '
 able to access Assessment B just by changing the UUID in the URL.'''

@login_required
def teacher_assessment_detail(request, assessment_id):

    if request.user.user_type != UserType.TEACHER:
        return redirect("admin:index")

    assessment = get_object_or_404(
        Assessment.objects.select_related(
            "program",
            "program__institute",
        ),
        id=assessment_id,
        created_by=request.user,
    )

    assessment_questions = (
        assessment.assessment_questions
        .select_related(
            "question",
            "question__chapter",
        )
        .order_by(
            "display_order",
        )
    )

    return render(
        request,
        "assessment/teacher_assessment_detail.html",
        {
            "assessment": assessment,
            "assessment_questions": assessment_questions,
        },
    )


@login_required
def teacher_assessment_add_questions(request, assessment_id):

    # -------------------------------------------------
    # 1. Only teachers
    # -------------------------------------------------

    if request.user.user_type != UserType.TEACHER:
        return redirect("admin:index")

    # -------------------------------------------------
    # 2. Get assessment owned by this teacher
    # -------------------------------------------------

    assessment = get_object_or_404(
        Assessment.objects.select_related(
            "program",
            "program__institute",
        ),
        id=assessment_id,
        created_by=request.user,
    )

    # -------------------------------------------------
    # 3. Published assessment cannot be modified
    # -------------------------------------------------

    if assessment.status != AssessmentStatus.DRAFT:

        messages.error(
            request,
            "Published assessments cannot be modified.",
        )

        return redirect(
            "teacher_assessment_detail",
            assessment_id=assessment.id,
        )

    # -------------------------------------------------
    # 4. Get teacher's questions for this program
    # -------------------------------------------------

    questions = (
        Question.objects
        .filter(
            chapter__subject__program=assessment.program,
            created_by=request.user,
            is_active=True,
            chapter__is_active=True,
            chapter__subject__is_active=True,
        )
        .select_related(
            "chapter",
        )
        .order_by(
            "chapter__name",
            "created_at",
        )
    )

    # -------------------------------------------------
    # 5. Existing questions
    # -------------------------------------------------

    existing_question_ids = set(
        assessment.assessment_questions.values_list(
            "question_id",
            flat=True,
        )
    )

    # -------------------------------------------------
    # 6. POST - Save selected questions
    # -------------------------------------------------

    if request.method == "POST":

        selected_question_ids = request.POST.getlist("questions")

        # -------------------------------------------------
        # Get valid questions
        # -------------------------------------------------

        valid_questions = questions.filter(
            id__in=selected_question_ids,
        )

        valid_question_ids = {
            str(question.id)
            for question in valid_questions
        }

        submitted_question_ids = set(
            selected_question_ids
        )

        # -------------------------------------------------
        # Security validation
        # -------------------------------------------------

        if submitted_question_ids != valid_question_ids:
            messages.error(
                request,
                "One or more selected questions are not valid "
                "for this assessment.",
            )

            return redirect(
                "teacher_assessment_add_questions",
                assessment_id=assessment.id,
            )

        # -------------------------------------------------
        # Synchronize questions
        # -------------------------------------------------

        with transaction.atomic():

            assessment.assessment_questions.exclude(
                question_id__in=valid_question_ids,
            ).delete()

            existing_question_ids = set(
                assessment.assessment_questions.values_list(
                    "question_id",
                    flat=True,
                )
            )

            current_max_order = (
                assessment.assessment_questions
                .order_by("-display_order")
                .values_list(
                    "display_order",
                    flat=True,
                )
                .first()
            ) or 0

            for question_id in selected_question_ids:

                question = valid_questions.get(
                    id=question_id
                )

                if question.id in existing_question_ids:
                    continue

                current_max_order += 1

                AssessmentQuestion.objects.create(
                    assessment=assessment,
                    question=question,
                    display_order=current_max_order,
                )

        # -------------------------------------------------
        # Rebuild display order
        # -------------------------------------------------

        assessment_questions = list(
            assessment.assessment_questions
            .order_by("display_order")
        )

        for index, assessment_question in enumerate(
            assessment_questions,
            start=1,
        ):

            if assessment_question.display_order != index:
                assessment_question.display_order = index

                assessment_question.save(
                    update_fields=[
                        "display_order",
                    ]
                )

        messages.success(
            request,
            "Assessment questions updated successfully.",
        )

        return redirect(
            "teacher_assessment_detail",
            assessment_id=assessment.id,
        )

    # -------------------------------------------------
    # 7. Display page
    # -------------------------------------------------

    return render(
        request,
        "assessment/teacher_assessment_add_questions.html",
        {
            "assessment": assessment,
            "questions": questions,
            "existing_question_ids": existing_question_ids,
        },
    )


@login_required
def teacher_assessment_publish(request, assessment_id):

    # -------------------------------------------------
    # 1. Only teachers
    # -------------------------------------------------

    if request.user.user_type != UserType.TEACHER:
        return redirect("admin:index")

    # -------------------------------------------------
    # 2. Get teacher's assessment
    # -------------------------------------------------

    assessment = get_object_or_404(
        Assessment.objects.select_related(
            "program",
        ),
        id=assessment_id,
        created_by=request.user,
    )

    # -------------------------------------------------
    # 3. Assessment must still be Draft
    # -------------------------------------------------

    if assessment.status != AssessmentStatus.DRAFT:

        messages.error(
            request,
            "This assessment has already been published.",
        )

        return redirect(
            "teacher_assessment_detail",
            assessment_id=assessment.id,
        )

    # -------------------------------------------------
    # 4. Must contain at least one question
    # -------------------------------------------------

    question_count = assessment.assessment_questions.count()

    if question_count == 0:

        messages.error(
            request,
            "You cannot publish an assessment without questions.",
        )

        return redirect(
            "teacher_assessment_detail",
            assessment_id=assessment.id,
        )

    # -------------------------------------------------
    # 5. Publish
    # -------------------------------------------------

    with transaction.atomic():

        assessment.status = AssessmentStatus.PUBLISHED
        assessment.is_active = True

        assessment.save(
            update_fields=[
                "status",
                "is_active",
                "updated_at",
            ]
        )

    messages.success(
        request,
        "Assessment published successfully.",
    )

    return redirect(
        "teacher_assessment_detail",
        assessment_id=assessment.id,
    )
