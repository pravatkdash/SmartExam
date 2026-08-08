from django import forms


class StudentOTPForm(forms.Form):
    otp = forms.CharField(
        max_length=4,
        min_length=4,
        label="OTP",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter 4-digit OTP",
                "autocomplete": "one-time-code",
                "inputmode": "numeric",
            }
        ),
    )

    def clean_otp(self):
        otp = self.cleaned_data["otp"].strip()

        if not otp.isdigit():
            raise forms.ValidationError(
                "OTP must contain only digits."
            )

        return otp