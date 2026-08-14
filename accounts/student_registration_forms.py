from django import forms


class StudentRegistrationForm(forms.Form):
    first_name = forms.CharField(
        max_length=150,
        label="First Name",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter your first name",
                "autocomplete": "given-name",
            }
        ),
    )

    email = forms.EmailField(
        required=False,
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Enter your email (optional)",
                "autocomplete": "email",
            }
        ),
    )

    pin = forms.CharField(
        min_length=4,
        max_length=4,
        label="PIN",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Enter 4-digit PIN",
                "inputmode": "numeric",
                "autocomplete": "new-password",
            }
        ),
    )

    confirm_pin = forms.CharField(
        min_length=4,
        max_length=4,
        label="Confirm PIN",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm 4-digit PIN",
                "inputmode": "numeric",
                "autocomplete": "new-password",
            }
        ),
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
            raise forms.ValidationError(
                "PIN and Confirm PIN must match."
            )

        return cleaned_data