import secrets
from datetime import timedelta

from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.utils import timezone

from .models import MobileOTP, OTPPurpose, EmailOTP


def generate_otp():
    return f"{secrets.randbelow(10000):04d}"


def create_otp(mobile_number, purpose):
    otp = generate_otp()

    MobileOTP.objects.filter(
        mobile_number=mobile_number,
        purpose=purpose,
        is_used=False,
    ).update(is_used=True)

    mobile_otp = MobileOTP.objects.create(
        mobile_number=mobile_number,
        otp_hash=make_password(otp),
        purpose=purpose,
        expires_at=timezone.now() + timedelta(minutes=5),
    )

    print(
        f"[SmartExam OTP] "
        f"{purpose} OTP for {mobile_number}: {otp}"
    )

    return mobile_otp

def verify_otp(mobile_number, otp, purpose):
    mobile_otp = (
        MobileOTP.objects
        .filter(
            mobile_number=mobile_number,
            purpose=purpose,
            is_used=False,
        )
        .order_by("-created_at")
        .first()
    )

    if not mobile_otp:
        return False, "OTP not found."

    if timezone.now() > mobile_otp.expires_at:
        return False, "OTP has expired."

    if mobile_otp.attempts >= 5:
        return False, "Maximum OTP attempts exceeded."

    if not check_password(otp, mobile_otp.otp_hash):
        mobile_otp.attempts += 1
        mobile_otp.save(update_fields=["attempts"])
        return False, "Invalid OTP."

    mobile_otp.is_used = True
    mobile_otp.save(update_fields=["is_used"])

    return True, "OTP verified successfully."


def create_email_otp(email, purpose):
    otp = generate_otp()

    EmailOTP.objects.filter(
        email=email,
        purpose=purpose,
        is_used=False,
    ).update(is_used=True)

    email_otp = EmailOTP.objects.create(
        email=email,
        otp_hash=make_password(otp),
        purpose=purpose,
        expires_at=timezone.now() + timedelta(minutes=5),
    )

    send_mail(
        subject="SmartExam Email Verification Code",
        message=(
            f"Your SmartExam verification code is: {otp}\n\n"
            "This code is valid for 5 minutes.\n"
            "If you did not request this code, please ignore this email."
        ),
        from_email=None,
        recipient_list=[email],
    )

    print(
        f"[SmartExam Email OTP] "
        f"{purpose} OTP for {email}: {otp}"
    )

    return email_otp

def verify_email_otp(email, otp, purpose):
    email_otp = (
        EmailOTP.objects
        .filter(
            email=email,
            purpose=purpose,
            is_used=False,
        )
        .order_by("-created_at")
        .first()
    )

    if not email_otp:
        return False, "OTP not found."

    if timezone.now() > email_otp.expires_at:
        return False, "OTP has expired."

    if email_otp.attempts >= 5:
        return False, "Maximum OTP attempts exceeded."

    if not check_password(otp, email_otp.otp_hash):
        email_otp.attempts += 1
        email_otp.save(update_fields=["attempts"])
        return False, "Invalid OTP."

    email_otp.is_used = True
    email_otp.save(update_fields=["is_used"])

    return True, "Email OTP verified successfully."