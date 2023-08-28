from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class CustomUserManager(BaseUserManager):

    def create_user(self, fullname, email, password, user_type='PATIENT', **extra_fields):
        if not email:
            raise ValueError(_("Email should be provided"))

        email = self.normalize_email(email)

        new_user = self.model(fullname=fullname, email=email, user_type=user_type, **extra_fields)

        new_user.set_password(password)

        new_user.save()

    def create_health_worker(self, fullname, email, password, **extra_fields):
        extra_fields.setdefault('user_type', 'HEALTH_WORKER')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', True)

        extra_fields.pop('specialization')
        extra_fields.pop('professional_title')

        return self.create_user(fullname, email, password, **extra_fields)

    def create_superuser(self, fullname, email, password, user_type='HEALTH_WORKER', **extra_field):

        extra_field.setdefault('is_staff', True)
        extra_field.setdefault('is_superuser', True)
        extra_field.setdefault('is_active', True)

        if extra_field.get('is_staff') is not True:
            raise ValueError(_("SuperUser should have is_staff = True"))

        if extra_field.get('is_superuser') is not True:
            raise ValueError(_("Superuser should have is_superuser = True"))

        if extra_field.get('is_active') is not True:
            raise ValueError(_("Superuser should have is_active = True"))

        return self.create_user(fullname, email, password, user_type, **extra_field)


class User(AbstractUser):
    USER_TYPES = [
        ('HEALTH_WORKER', 'health_worker'),
        ('PATIENT', 'patient')
    ]

    fullname = models.CharField(max_length=30, null=False)
    email = models.EmailField(max_length=50, unique=True)

    # Add unique related_name attributes for groups and user_permissions fields
    groups = models.ManyToManyField(
        Group,
        related_name="custom_users",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_users",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )
    phone_number = PhoneNumberField(null=False, unique=True)
    user_type = models.CharField(max_length=15, choices=USER_TYPES, default='PATIENT')
    emergency_contact_name = models.CharField(max_length=30, null=False)
    emergency_contact_number = PhoneNumberField(null=False, unique=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['fullname', 'phone_number']

    objects = CustomUserManager()

    def __str__(self):
        return f"<User {self.email}>"
