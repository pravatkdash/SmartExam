from django import forms


class StudentLoginForm(forms.Form):
    mobile_number = forms.CharField(
        max_length=15,
        min_length=10,
        label="Mobile Number",
    )

    pin = forms.CharField(
        min_length=4,
        max_length=4,
        label="PIN",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Enter 4-digit PIN",
                "inputmode": "numeric",
                "autocomplete": "current-password",
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

    def clean_pin(self):
        pin = self.cleaned_data["pin"]

        if not pin.isdigit():
            raise forms.ValidationError(
                "PIN must contain only digits."
            )

        return pin