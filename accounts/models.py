from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager as BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError
        if not password:
            raise ValueError
        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        if not extra_fields.setdefault('is_staff', True):
            raise ValueError
        if not extra_fields.setdefault('is_superuser', True):
            raise ValueError
        return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField()
    username = models.CharField(max_length=128)
    is_staff = models.BooleanField()
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
    def __str__(self):
        return self.email

    @property
    def is_admin(self):
        return self.is_superuser
