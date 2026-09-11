from django import forms
from django.contrib import admin, messages
from django.db import models, transaction


from .models import Question, Option
from .admin_forms import QuestionAdminForm, OptionInlineFormSet, OptionAdminForm
from .question_service import is_question_locked, get_question_lock_message


class OptionInline(admin.TabularInline):
    model = Option
    form = OptionAdminForm
    formset = OptionInlineFormSet

    extra = 4

    verbose_name = "Possible Answer"
    verbose_name_plural = "Possible Answers"

    exclude = (
        "display_order",
        "is_active",
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
    )

    formfield_overrides = {
        models.TextField: {
            "widget": forms.Textarea(
                attrs={
                    "rows": 4,
                    "cols": 100,
                }
            )
        }
    }

    def get_readonly_fields(self, request, obj=None):
        if obj and is_question_locked(obj):
            return (
                "question",
                "option_text",
                "is_correct",
                "display_order",
            )

        return ()

    def has_delete_permission(self, request, obj=None):
        if obj and is_question_locked(obj):
            return False

        return super().has_delete_permission(request, obj)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    form = QuestionAdminForm

    list_display = (
        "chapter",
        "question_preview",
        "difficulty",
        "marks",
        "is_active",
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        if request.user.user_type == "TEACHER":
            assigned_subject_ids = request.user.teacher_assignments.filter(
                is_active=True,
            ).values_list(
                "subject_id",
                flat=True,
            )

            form.base_fields["chapter"].queryset = (
                form.base_fields["chapter"]
                .queryset
                .filter(subject_id__in=assigned_subject_ids)
            )

        return form

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user

        super().save_model(request, obj, form, change)

    @admin.display(description="Question")
    def question_preview(self, obj):
        return obj.question_text

    search_fields = (
        "question_text",
    )

    list_filter = (
        "difficulty",
        "chapter",
        "is_active",
    )

    fieldsets = (
        (
            "Question Information",
            {
                "fields": (
                    "chapter",
                    "question_text",
                    "explanation",
                )
            },
        ),
        (
            "Scoring",
            {
                "fields": (
                    "difficulty",
                    (
                        "marks",
                        "negative_marks",
                    ),
                )
            },
        ),
        (
            "Settings",
            {
                "fields": (
                    "is_multiple_answer",
                )
            },
        ),
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    inlines = [
        OptionInline,
    ]

    def get_fieldsets(self, request, obj=None):
        """
        Show audit information only while editing.
        """
        fieldsets = list(super().get_fieldsets(request, obj))

        if obj:
            fieldsets.append(
                (
                    "Audit Information",
                    {
                        "fields": (
                            "created_at",
                            "updated_at",
                        )
                    },
                )
            )

        return fieldsets


    def save_formset(self, request, form, formset, change):

        with transaction.atomic():

            # Let Django prepare the formset.
            # This also populates formset.deleted_objects.
            instances = formset.save(commit=False)

            # Delete options marked for deletion
            for obj in formset.deleted_objects:
                obj.delete()

            question = form.instance

            # --------------------------------------------------
            # STEP 1: Get ALL remaining options in form order
            # --------------------------------------------------

            options = []

            for inline_form in formset.forms:

                if not inline_form.cleaned_data:
                    continue

                if inline_form.cleaned_data.get("DELETE", False):
                    continue

                option = inline_form.instance

                # Ignore empty extra forms
                if not option.option_text:
                    continue

                options.append(option)

            # --------------------------------------------------
            # STEP 2: Move existing options to temporary orders
            # --------------------------------------------------

            existing_options = list(
                question.options.all()
            )

            max_order = (
                    question.options.aggregate(
                        max_order=models.Max("display_order")
                    )["max_order"]
                    or 0
            )

            temp_order = max_order + 1

            for option in existing_options:
                option.display_order = temp_order
                option.save(update_fields=["display_order"])
                temp_order += 1

            # --------------------------------------------------
            # STEP 3: Save new options with temporary orders
            # --------------------------------------------------

            for instance in instances:
                # Only new/changed instances are returned here
                instance.display_order = temp_order
                instance.save()
                temp_order += 1

            # --------------------------------------------------
            # STEP 4: Assign final display order
            # --------------------------------------------------

            for order, option in enumerate(options, start=1):
                option.display_order = order
                option.save(
                    update_fields=["display_order"]
                )

            formset.save_m2m()



    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj))

        if obj and is_question_locked(obj):
            readonly_fields.extend([
                "chapter",
                "question_text",
                "explanation",
                "difficulty",
                "marks",
                "negative_marks",
                "is_multiple_answer",
            ])

        return tuple(readonly_fields)

    def has_delete_permission(self, request, obj=None):
        if obj and is_question_locked(obj):
            return False

        return super().has_delete_permission(request, obj)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        try:
            obj = self.get_object(request, object_id)

            if obj and is_question_locked(obj):
                message = get_question_lock_message(obj)

                messages.warning(
                    request,
                    f"🔒 Question Locked: {message}"
                )

        except Exception:
            pass

        return super().change_view(
            request,
            object_id,
            form_url,
            extra_context,
        )


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):

    list_display = (
        "question",
        "display_order",
        "option_text",
        "is_correct",
    )

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(
            super().get_readonly_fields(request, obj)
        )

        if obj and is_question_locked(obj):
            readonly_fields.extend([
                "chapter",
                "question_text",
                "explanation",
                "difficulty",
                "marks",
                "negative_marks",
                "is_multiple_answer",
            ])

        return tuple(readonly_fields)

    def has_delete_permission(self, request, obj=None):
        if obj and is_question_locked(obj.question):
            return False

        return super().has_delete_permission(request, obj)