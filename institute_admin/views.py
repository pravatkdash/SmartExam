from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render, get_object_or_404

from accounts.models import User, UserType
from institute_admin.forms.student import StudentCreateForm
from institute_admin.forms.teacher import TeacherCreateForm
from institute_admin.forms.teacher_assignment import TeacherAssignmentForm
from subjects.models import StudentProgramEnrollment


@login_required
def dashboard(request):
    if request.user.user_type != UserType.INSTITUTE_ADMIN:
        return redirect("home")

    return render(
        request,
        "institute_admin/dashboard.html",
    )


@login_required
def teacher_list(request):
    if request.user.user_type != UserType.INSTITUTE_ADMIN:
        return redirect("home")

    teachers = (
        User.objects
        .filter(
            institute=request.user.institute,
            user_type=UserType.TEACHER,
        )
        .order_by("first_name", "last_name")
    )

    return render(
        request,
        "institute_admin/teacher_list.html",
        {
            "teachers": teachers,
        },
    )



@login_required
def teacher_create(request):
    if request.user.user_type != UserType.INSTITUTE_ADMIN:
        return redirect("home")

    if request.method == "POST":
        form = TeacherCreateForm(request.POST)

        if form.is_valid():
            teacher = form.save(commit=False)

            teacher.user_type = UserType.TEACHER
            teacher.institute = request.user.institute

            teacher.set_password(
                form.cleaned_data["password"]
            )

            teacher.save()

            return redirect("institute_teacher_list")

    else:
        form = TeacherCreateForm()

    return render(
        request,
        "institute_admin/teacher_create.html",
        {
            "form": form,
        },
    )



@login_required
def teacher_assignment(request, teacher_id):
    if request.user.user_type != UserType.INSTITUTE_ADMIN:
        return redirect("home")

    teacher = get_object_or_404(
        User,
        id=teacher_id,
        user_type=UserType.TEACHER,
        institute=request.user.institute,
    )

    assignments = (
        teacher.teacher_assignments
        .filter(is_active=True)
        .select_related(
            "subject",
            "chapter",
            "chapter__subject",
        )
    )

    if request.method == "POST":

        form = TeacherAssignmentForm(
            request.POST,
            institute=request.user.institute,
        )

        # Set teacher before model validation
        form.instance.teacher = teacher

        if form.is_valid():

            form.save()

            return redirect(
                "institute_teacher_assignment",
                teacher_id=teacher.id,
            )

    else:

        form = TeacherAssignmentForm(
            institute=request.user.institute,
        )

    return render(
        request,
        "institute_admin/teacher_assignment.html",
        {
            "teacher": teacher,
            "assignments": assignments,
            "form": form,
        },
    )


@login_required
def student_list(request):
    if request.user.user_type != UserType.INSTITUTE_ADMIN:
        return redirect("home")

    students = (
        User.objects
        .filter(
            institute=request.user.institute,
            user_type=UserType.STUDENT,
        )
        .order_by("first_name", "last_name")
    )

    return render(
        request,
        "institute_admin/student_list.html",
        {
            "students": students,
        },
    )


@login_required
def student_create(request):
    if request.user.user_type != UserType.INSTITUTE_ADMIN:
        return redirect("home")

    if request.method == "POST":
        form = StudentCreateForm(
            request.POST,
            institute=request.user.institute,
        )

        if form.is_valid():
            with transaction.atomic():
                student = form.save(commit=False)

                student.user_type = UserType.STUDENT
                student.institute = request.user.institute

                student.set_password(
                    form.cleaned_data["pin"]
                )
                student.mobile_verified = True

                student.save()

                programs = form.cleaned_data["programs"]

                StudentProgramEnrollment.objects.bulk_create(
                    [
                        StudentProgramEnrollment(
                            student=student,
                            program=program,
                        )
                        for program in programs
                    ]
                )

            return redirect("institute_student_list")

    else:
        form = StudentCreateForm(
            institute=request.user.institute,
        )

    return render(
        request,
        "institute_admin/student_create.html",
        {
            "form": form,
        },
    )