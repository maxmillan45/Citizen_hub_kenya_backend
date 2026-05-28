from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('Phone number is required')
        user = self.model(phone_number=phone_number, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone_number, password, **extra_fields)

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    national_id_hash = models.CharField(max_length=64, blank=True, null=True)
    is_id_verified = models.BooleanField(default=False)
    civic_score = models.IntegerField(default=0)
    account_type = models.CharField(max_length=20, default='free')
    language = models.CharField(max_length=5, default='en')
    created_at = models.DateTimeField(default=timezone.now)
    last_active = models.DateTimeField(auto_now=True)

    username = None
    email = None

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.phone_number

