from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from accounts.models import User, UserType
from institute_admin.forms.teacher import TeacherCreateForm
from institute_admin.forms.teacher_assignment import TeacherAssignmentForm


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