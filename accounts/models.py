from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from core.models.base_model import BaseModel


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser, BaseModel):
    username = None
    email = models.EmailField(
        unique=True, error_messages={"unique": "Email already exists!"}
    )
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # No extra fields required

    objects = CustomUserManager()  # ✅ Use custom manager

    def __str__(self):
        return f"{self.email} -- {self.phone}"
