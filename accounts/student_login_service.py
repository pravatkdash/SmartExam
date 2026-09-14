from .models import User, UserType


def authenticate_student(mobile_number, pin):
    try:
        student = User.objects.get(
            mobile_number=mobile_number,
            user_type=UserType.STUDENT,
        )
        print(student)
    except User.DoesNotExist:
        print("Student not found")
        return None

    if not student.is_active:
        print("Student not active")
        return None

    if not student.mobile_verified:
        print("Student not verified")
        return None

    if not student.check_password(pin):
        print("Student password incorrect")
        return None

    return student