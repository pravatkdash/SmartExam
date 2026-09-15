from django.db import transaction

from .models import User, UserType


from django.db import transaction

from accounts.models import User, UserType
from subjects.models import Program, StudentProgramEnrollment


@transaction.atomic
def register_student(
    mobile_number,
    first_name,
    pin,
    email=None,
):
    if User.objects.filter(mobile_number=mobile_number).exists():
        raise ValueError("A user with this mobile number already exists.")

    if email and User.objects.filter(email=email).exists():
        raise ValueError("A user with this email already exists.")

    student = User.objects.create_user(
        email=email,
        password=pin,
        first_name=first_name,
        mobile_number=mobile_number,
        user_type=UserType.STUDENT,
        mobile_verified=True,
    )

    # -------------------------------------------------
    # Automatically enroll student in SmartExam
    # default programs.
    #
    # SmartExam programs have institute=None.
    # -------------------------------------------------

    default_programs = Program.objects.filter(
        institute__isnull=True,
        is_active=True,
    )

    StudentProgramEnrollment.objects.bulk_create(
        [
            StudentProgramEnrollment(
                student=student,
                program=program,
                is_active=True,
            )
            for program in default_programs
        ]
    )

    return student