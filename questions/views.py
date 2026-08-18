from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, get_object_or_404, render

from accounts.models import UserType
from questions.models import Question
from questions.question_service import is_question_locked, get_question_lock_message
from questions.teacher_forms import TeacherQuestionForm, TeacherOptionFormSet
from subjects.models import TeacherAssignment


@login_required
def teacher_edit_question(
        request,
        subject_id,
        chapter_id,
        question_id,
):
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




# Create your views here.
