import secrets
from datetime import timedelta

from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone

from .models import MobileOTP, OTPPurpose


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