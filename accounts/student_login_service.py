from .models import User, UserType


def authenticate_student(mobile_number, pin):
    try:
        student = User.objects.get(
            mobile_number=mobile_number,
            user_type=UserType.STUDENT,
        )
    except User.DoesNotExist:
        return None

    if not student.is_active:
        return None

    if not student.mobile_verified:
        return None

    if not student.check_password(pin):
        return None

    return student