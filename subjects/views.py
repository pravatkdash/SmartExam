from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from accounts.models import UserType
from .models import Program, Subject, Chapter


@login_required
def institute_dashboard(request):
    if request.user.user_type != UserType.INSTITUTE_ADMIN:
        return redirect("home")

    return render(
        request,
        "subjects/institute_dashboard.html",
    )


@login_required
def institute_program_list(request):
    if request.user.user_type != UserType.INSTITUTE_ADMIN:
        return redirect("home")

    programs = (
        Program.objects
        .filter(
            institute=request.user.institute,
            is_active=True,
        )
        .order_by("name")
    )

    return render(
        request,
        "subjects/institute_program_list.html",
        {
            "programs": programs,
        },
    )


@login_required
def institute_program_create(request):
    if request.user.user_type != UserType.INSTITUTE_ADMIN:
        return redirect("home")

    if request.method == "POST":

        name = request.POST.get("name", "").strip()
        description = request.POST.get("description", "").strip()

        if name:

            Program.objects.create(
                institute=request.user.institute,
                name=name,
                description=description,
            )

            return redirect("institute_program_list")

    return render(
        request,
        "subjects/institute_program_create.html",
    )


@login_required
def institute_program_subject_list(request, program_id):

    if request.user.user_type != UserType.INSTITUTE_ADMIN:
        return redirect("home")

    program = get_object_or_404(
        Program,
        id=program_id,
        institute=request.user.institute,
        is_active=True,
    )

    subjects = (
        Subject.objects
        .filter(
            program=program,
            is_active=True,
        )
        .order_by("name")
    )

    return render(
        request,
        "subjects/institute_program_subject_list.html",
        {
            "program": program,
            "subjects": subjects,
        },
    )



@login_required
def institute_subject_chapter_list(request, program_id, subject_id):

    if request.user.user_type != UserType.INSTITUTE_ADMIN:
        return redirect("home")

    program = get_object_or_404(
        Program,
        id=program_id,
        institute=request.user.institute,
        is_active=True,
    )

    subject = get_object_or_404(
        Subject,
        id=subject_id,
        program=program,
        is_active=True,
    )

    chapters = (
        Chapter.objects
        .filter(
            subject=subject,
        )
        .order_by("name")
    )

    return render(
        request,
        "subjects/institute_subject_chapter_list.html",
        {
            "program": program,
            "subject": subject,
            "chapters": chapters,
        },
    )



@login_required
def institute_subject_create(request, program_id):

    if request.user.user_type != UserType.INSTITUTE_ADMIN:
        return redirect("home")

    program = get_object_or_404(
        Program,
        id=program_id,
        institute=request.user.institute,
        is_active=True,
    )

    if request.method == "POST":

        name = request.POST.get("name", "").strip()
        description = request.POST.get("description", "").strip()

        if name:

            Subject.objects.create(
                program=program,
                name=name,
                description=description,
            )

            return redirect(
                "institute_program_subject_list",
                program_id=program.id,
            )

    return render(
        request,
        "subjects/institute_subject_create.html",
        {
            "program": program,
        },
    )


@login_required
def institute_subject_chapter_create(request, program_id, subject_id):

    if request.user.user_type != UserType.INSTITUTE_ADMIN:
        return redirect("home")

    program = get_object_or_404(
        Program,
        id=program_id,
        institute=request.user.institute,
        is_active=True,
    )

    subject = get_object_or_404(
        Subject,
        id=subject_id,
        program=program,
        is_active=True,
    )

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        description = request.POST.get("description", "").strip()

        if name:
            Chapter.objects.create(
                subject=subject,
                name=name,
                description=description,
            )

            return redirect(
                "institute_subject_chapter_list",
                program_id=program.id,
                subject_id=subject.id,
            )

    return render(
        request,
        "subjects/institute_subject_chapter_create.html",
        {
            "program": program,
            "subject": subject,
        },
    )