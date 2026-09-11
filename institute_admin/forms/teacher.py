from django import forms

from accounts.models import User


class TeacherCreateForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput,
        min_length=8,
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        min_length=8,
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "mobile_number",
        )

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error(
                "confirm_password",
                "Passwords do not match.",
            )

        return cleaned_data