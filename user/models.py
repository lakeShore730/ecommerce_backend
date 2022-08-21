from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager
from django.utils import timezone
from .validators import validate_otp_number, validate_phone_number


# Custom user model

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now, editable=False)
    location = models.CharField(max_length=100, blank=True, default="")
    phone_number = models.CharField(max_length=10, blank=True, null=True, validators=[validate_phone_number])
    updated_at = models.DateTimeField(default=timezone.now)
    profile_image = models.ImageField(upload_to='profile_images', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


# OTP to make active and verify a user  

class RegisterUserOtp (models.Model):
    otp = models.CharField(max_length=6, unique=True, validators=[validate_otp_number])
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.user.email


# OTP for the forgot password 

class ForgotPasswordOtp(models.Model):
    otp = models.CharField(max_length=6, unique=True, validators=[validate_otp_number])
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.user.email

