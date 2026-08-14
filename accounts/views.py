from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.

from django.http import HttpResponse

from accounts.mobile_number_forms import StudentMobileForm
from accounts.models import OTPPurpose, UserType
from accounts.otp_forms import StudentOTPForm
from accounts.otp_service import create_otp, verify_otp
from accounts.registration_service import register_student
from accounts.student_login_forms import StudentLoginForm
from accounts.student_login_service import authenticate_student
from accounts.student_registration_forms import StudentRegistrationForm
from assessment.models import Assessment, AssessmentAttempt, AssessmentAttemptStatus


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


def student_logout(request):
    logout(request)
    return redirect("student_login")