from django import forms

from accounts.models import User, UserType


class UserAdminForm(forms.ModelForm):

    class Meta:
        model = User
        fields = "__all__"
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.user_type != UserType.INSTITUTE_ADMIN:
            self.fields.pop("institute", None)

    def clean(self):
        cleaned_data = super().clean()

        user_type = cleaned_data.get("user_type")
        institute = cleaned_data.get("institute")

        if user_type == UserType.INSTITUTE_ADMIN and not institute:
            self.add_error(
                "institute",
                "Institute is required for an Institute Admin.",
            )

        if user_type != UserType.INSTITUTE_ADMIN and institute:
            self.add_error(
                "institute",
                "Only an Institute Admin can be assigned to an institute.",
            )

        return cleaned_data
    """



class TeacherLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "autofocus": True,
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
            }
        )
    )



