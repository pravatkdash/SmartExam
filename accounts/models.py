import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import UserManager


class UserType(models.TextChoices):
    SUPER_ADMIN = "SUPER_ADMIN", "Super Admin"
    ADMIN = "ADMIN", "Admin"
    TEACHER = "TEACHER", "Teacher"
    STUDENT = "STUDENT", "Student"


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    username = None

    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15, unique=True)

    user_type = models.CharField(
        max_length=20,
        choices=UserType.choices,
        default=UserType.STUDENT,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "mobile_number"]
    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"