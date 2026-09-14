from django import forms
from django.db.models import Q

from accounts.models import User
from subjects.models import Program


class StudentCreateForm(forms.ModelForm):

    pin = forms.CharField(
        widget=forms.PasswordInput,
        min_length=4,
        max_length=4,
        label="PIN",
    )

    confirm_pin = forms.CharField(
        widget=forms.PasswordInput,
        min_length=4,
        max_length=4,
        label="Confirm PIN",
    )

    programs = forms.ModelMultipleChoiceField(
        queryset=Program.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Programs",
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "mobile_number",
        )

    def __init__(self, *args, institute=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["programs"].queryset = (
            Program.objects.filter(
                is_active=True,
            )
            .filter(
                Q(institute__isnull=True)
                | Q(institute=institute)
            )
            .order_by("institute__name", "name")
        )

    def clean_pin(self):
        pin = self.cleaned_data["pin"]

        if not pin.isdigit():
            raise forms.ValidationError(
                "PIN must contain only digits."
            )

        return pin

    def clean_confirm_pin(self):
        confirm_pin = self.cleaned_data["confirm_pin"]

        if not confirm_pin.isdigit():
            raise forms.ValidationError(
                "PIN must contain only digits."
            )

        return confirm_pin

    def clean(self):
        cleaned_data = super().clean()

        pin = cleaned_data.get("pin")
        confirm_pin = cleaned_data.get("confirm_pin")

        if pin and confirm_pin and pin != confirm_pin:
            self.add_error(
                "confirm_pin",
                "PINs do not match.",
            )

        return cleaned_data