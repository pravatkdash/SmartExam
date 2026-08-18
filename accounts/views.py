from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.

from django.http import HttpResponse

from accounts.forms import TeacherLoginForm
from accounts.mobile_number_forms import StudentMobileForm
from accounts.models import OTPPurpose, UserType
from accounts.otp_forms import StudentOTPForm
from accounts.otp_service import create_otp, verify_otp
from accounts.registration_service import register_student
from accounts.student_login_forms import StudentLoginForm
from accounts.student_login_service import authenticate_student
from accounts.student_registration_forms import StudentRegistrationForm
from assessment.models import Assessment, AssessmentAttempt, AssessmentAttemptStatus
from questions.models import Question
from questions.question_service import is_question_locked, get_question_lock_message
from questions.teacher_forms import TeacherQuestionForm, TeacherOptionAddFormSet, TeacherOptionFormSet
from subjects.models import TeacherAssignment


def home(request):
    return render(request, "accounts/home.html")

def student_register(request):
    if request.method == "POST":
        form = StudentMobileForm(request.POST)

        if form.is_valid():
            mobile_number = form.cleaned_data["mobile_number"]

            create_otp(
                mobile_number,
                OTPPurpose.REGISTRATION,
            )

            request.session["registration_mobile"] = mobile_number

            return redirect("student_verify_otp")

    else:
        form = StudentMobileForm()

    return render(
        request,
        "accounts/student_register.html",
        {"form": form},
    )

def student_verify_otp(request):
    mobile_number = request.session.get("registration_mobile")

    if not mobile_number:
        return redirect("student_register")

    if request.method == "POST":
        form = StudentOTPForm(request.POST)

        if form.is_valid():
            otp = form.cleaned_data["otp"]

            success, message = verify_otp(
                mobile_number,
                otp,
                OTPPurpose.REGISTRATION,
            )

            if success:
                request.session["registration_mobile_verified"] = True
                return redirect("student_registration_details")

            form.add_error("otp", message)

    else:
        form = StudentOTPForm()

    return render(
        request,
        "accounts/student_verify_otp.html",
        {"form": form},
    )


def student_registration_details(request):
    mobile_number = request.session.get("registration_mobile")
    mobile_verified = request.session.get("registration_mobile_verified")

    if not mobile_number or not mobile_verified:
        return redirect("student_register")

    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)

        if form.is_valid():
            try:
                register_student(
                    mobile_number=mobile_number,
                    first_name=form.cleaned_data["first_name"],
                    pin=form.cleaned_data["pin"],
                    email=form.cleaned_data["email"] or None,
                )

                # Registration completed.
                request.session.pop("registration_mobile", None)
                request.session.pop("registration_mobile_verified", None)

                return redirect("student_registration_success")

            except ValueError as exc:
                form.add_error(None, str(exc))

    else:
        form = StudentRegistrationForm()

    return render(
        request,
        "accounts/student_registration_details.html",
        {"form": form},
    )


def student_registration_success(request):
    return render(
        request,
        "accounts/student_registration_success.html",
    )


def student_login(request):

    if request.user.is_authenticated:
        if request.user.user_type == UserType.STUDENT:
            return redirect("student_dashboard")

        return redirect("home")

    if request.method == "POST":
        form = StudentLoginForm(request.POST)

        if form.is_valid():
            student = authenticate_student(
                mobile_number=form.cleaned_data["mobile_number"],
                pin=form.cleaned_data["pin"],
            )

            if student:
                login(request, student)
                return redirect("student_dashboard")

            form.add_error(
                None,
                "Invalid mobile number or PIN.",
            )

    else:
        form = StudentLoginForm()

    return render(
        request,
        "accounts/student_login.html",
        {"form": form},
    )



@login_required
def student_dashboard(request):

    if request.user.user_type != UserType.STUDENT:
        return redirect("home")

    assessments = Assessment.objects.filter(
        status="PUBLISHED",
        is_active=True,
    ).order_by("name")

    for assessment in assessments:

        assessment.current_attempt = (
            AssessmentAttempt.objects
            .filter(
                student=request.user,
                assessment=assessment,
                status=AssessmentAttemptStatus.IN_PROGRESS,
            )
            .order_by("-started_at")
            .first()
        )

        assessment.last_submitted_attempt = (
            AssessmentAttempt.objects
            .filter(
                student=request.user,
                assessment=assessment,
                status=AssessmentAttemptStatus.SUBMITTED,
            )
            .order_by("-submitted_at")
            .first()
        )

    return render(
        request,
        "accounts/student_dashboard.html",
        {
            "assessments": assessments,
        },
    )


def teacher_login(request):
    if request.user.is_authenticated:
        if request.user.user_type == UserType.TEACHER:
            return redirect("teacher_dashboard")

        return redirect("admin:index")

    if request.method == "POST":
        form = TeacherLoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = authenticate(
                request,
                email=email,
                password=password,
            )

            if user is not None and user.user_type == UserType.TEACHER:
                login(request, user)
                return redirect("teacher_dashboard")

            messages.error(
                request,
                "Invalid teacher credentials.",
            )
    else:
        form = TeacherLoginForm()

    return render(
        request,
        "accounts/teacher_login.html",
        {
            "form": form,
        },
    )



def teacher_dashboard(request):
    if not request.user.is_authenticated:
        return redirect("teacher_login")

    if request.user.user_type != UserType.TEACHER:
        return redirect("admin:index")

    assignments = (
        request.user.teacher_assignments
        .filter(
            is_active=True,
            subject__is_active=True,
        )
        .select_related(
            "subject",
            "subject__program",
            "subject__program__institute",
        )
    )

    return render(
        request,
        "accounts/teacher_dashboard.html",
        {
            "assignments": assignments,
        },
    )


def teacher_subject_chapters(request, subject_id):
    if not request.user.is_authenticated:
        return redirect("teacher_login")

    if request.user.user_type != UserType.TEACHER:
        return redirect("admin:index")

    assignment = get_object_or_404(
        TeacherAssignment,
        teacher=request.user,
        subject_id=subject_id,
        is_active=True,
        subject__is_active=True,
    )

    subject = assignment.subject

    chapters = subject.chapters.filter(
        is_active=True,
    ).order_by("name")

    return render(
        request,
        "accounts/teacher_subject_chapters.html",
        {
            "subject": subject,
            "chapters": chapters,
        },
    )


@login_required
def teacher_chapter_questions(request, subject_id, chapter_id):

    if request.user.user_type != UserType.TEACHER:
        return redirect("admin:index")

    assignment = get_object_or_404(
        TeacherAssignment,
        teacher=request.user,
        subject_id=subject_id,
        is_active=True,
        subject__is_active=True,
    )

    chapter = get_object_or_404(
        assignment.subject.chapters,
        id=chapter_id,
        is_active=True,
    )

    questions = (
        Question.objects
        .filter(
            chapter=chapter,
            created_by=request.user,
        )
        .order_by("created_at")
    )

    return render(
        request,
        "accounts/teacher_chapter_questions.html",
        {
            "subject": assignment.subject,
            "chapter": chapter,
            "questions": questions,
        },
    )


@login_required
def teacher_question_detail(request, subject_id, chapter_id, question_id):

    if request.user.user_type != UserType.TEACHER:
        return redirect("admin:index")

    assignment = get_object_or_404(
        TeacherAssignment,
        teacher=request.user,
        subject_id=subject_id,
        is_active=True,
        subject__is_active=True,
    )

    chapter = get_object_or_404(
        assignment.subject.chapters,
        id=chapter_id,
        is_active=True,
    )

    question = get_object_or_404(
        Question.objects.prefetch_related("options"),
        id=question_id,
        chapter=chapter,
        created_by=request.user,
    )

    question_locked = is_question_locked(question)

    return render(
        request,
        "accounts/teacher_question_detail.html",
        {
            "subject": assignment.subject,
            "chapter": chapter,
            "question": question,
            "question_locked": question_locked,
        },
    )



@login_required
def teacher_add_question(request, subject_id, chapter_id):

    if request.user.user_type != UserType.TEACHER:
        return redirect("admin:index")

    assignment = get_object_or_404(
        TeacherAssignment,
        teacher=request.user,
        subject_id=subject_id,
        is_active=True,
        subject__is_active=True,
    )

    chapter = get_object_or_404(
        assignment.subject.chapters,
        id=chapter_id,
        is_active=True,
    )

    if request.method == "POST":

        question_form = TeacherQuestionForm(
            request.POST
        )

        # Temporary Question object used only for
        # validating the inline formset.
        temporary_question = Question(
            chapter=chapter,
            created_by=request.user,
        )

        question_formset = TeacherOptionAddFormSet(
            request.POST,
            instance=temporary_question,
        )

        if (
            question_form.is_valid()
            and question_formset.is_valid()
        ):

            with transaction.atomic():

                # ---------------------------------
                # 1. Save the Question first
                # ---------------------------------

                question = question_form.save(
                    commit=False
                )

                question.chapter = chapter
                question.created_by = request.user

                question.save()

                # ---------------------------------
                # 2. Create a NEW formset using
                #    the SAVED Question
                # ---------------------------------

                question_formset = TeacherOptionAddFormSet(
                    request.POST,
                    instance=question,
                )

                if not question_formset.is_valid():
                    raise ValueError(
                        "Option formset became invalid "
                        "after saving the question."
                    )

                # ---------------------------------
                # 3. Save Options
                # ---------------------------------

                question_formset.save()

            messages.success(
                request,
                "Question created successfully.",
            )

            return redirect(
                "teacher_chapter_questions",
                subject_id=subject_id,
                chapter_id=chapter_id,
            )

    else:

        question_form = TeacherQuestionForm()

        question = Question(
            chapter=chapter,
            created_by=request.user,
        )

        question_formset = TeacherOptionAddFormSet(
            instance=question,
        )

    return render(
        request,
        "accounts/teacher_add_question.html",
        {
            "question_form": question_form,
            "question_formset": question_formset,
            "subject": assignment.subject,
            "chapter": chapter,
        },
    )



@login_required
def teacher_edit_question(
    request,
    subject_id,
    chapter_id,
    question_id,
):

    if request.user.user_type != UserType.TEACHER:
        return redirect("admin:index")

    # Verify that this teacher is assigned to the subject.
    assignment = get_object_or_404(
        TeacherAssignment,
        teacher=request.user,
        subject_id=subject_id,
        is_active=True,
        subject__is_active=True,
    )

    # Verify that the chapter belongs to the subject.
    chapter = get_object_or_404(
        assignment.subject.chapters,
        id=chapter_id,
        is_active=True,
    )

    # Verify that the question belongs to this chapter
    # and was created by this teacher.
    question = get_object_or_404(
        Question.objects.prefetch_related("options"),
        id=question_id,
        chapter=chapter,
        created_by=request.user,
    )

    # Published assessment questions are immutable.
    if is_question_locked(question):

        messages.error(
            request,
            get_question_lock_message(question),
        )

        return redirect(
            "teacher_question_detail",
            subject_id=subject_id,
            chapter_id=chapter_id,
            question_id=question_id,
        )

    if request.method == "POST":

        question_form = TeacherQuestionForm(
            request.POST,
            instance=question,
        )

        question_formset = TeacherOptionFormSet(
            request.POST,
            instance=question,
        )

        if (
            question_form.is_valid()
            and question_formset.is_valid()
        ):

            with transaction.atomic():

                question_form.save()
                question_formset.save()

            messages.success(
                request,
                "Question updated successfully.",
            )

            return redirect(
                "teacher_question_detail",
                subject_id=subject_id,
                chapter_id=chapter_id,
                question_id=question_id,
            )

    else:

        question_form = TeacherQuestionForm(
            instance=question,
        )

        question_formset = TeacherOptionFormSet(
            instance=question,
        )

    return render(
        request,
        "accounts/teacher_edit_question.html",
        {
            "question_form": question_form,
            "question_formset": question_formset,
            "subject": assignment.subject,
            "chapter": chapter,
            "question": question,
        },
    )


def student_logout(request):
    logout(request)
    return redirect("student_login")