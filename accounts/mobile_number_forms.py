from django import forms

from accounts.models import User


class StudentMobileForm(forms.Form):
    mobile_number = forms.CharField(
        max_length=15,
        min_length=10,
        label="Mobile Number",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter mobile number",
                "autocomplete": "tel",
                "inputmode": "numeric",
            }
        ),
    )

    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Enter your email address",
                "autocomplete": "email",
            }
        ),
    )

    def clean_mobile_number(self):
        mobile_number = self.cleaned_data["mobile_number"].strip()

        if not mobile_number.isdigit():
            raise forms.ValidationError(
                "Mobile number must contain only digits."
            )

        if len(mobile_number) != 10:
            raise forms.ValidationError(
                "Enter a valid 10-digit mobile number."
            )

        return mobile_number

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "An account with this email address already exists."
            )

        return email