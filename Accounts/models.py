from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import date, datetime, timedelta
import os


class MyUser(AbstractUser):
    """
    Custom User model.
    Public users authenticate via PHONE + OTP.
    Username exists ONLY for Django internals & admin login.
    """

    phone = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)
    # Remove unused fields
    email = models.EmailField(null=True, blank=True)
    first_name = None
    last_name = None

    server_id = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        unique=True
    )

    doj = models.DateField(default=date.today)

    profile = models.ImageField(upload_to="profile/", null=True, blank=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["phone", "name"]

    def save(self, *args, **kwargs):
        if not self.server_id:
            self.server_id = generate_server_id()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.profile and os.path.isfile(self.profile.path):
            os.remove(self.profile.path)
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.server_id if self.server_id else self.username


class LoginOTP(models.Model):
    phone = models.CharField(max_length=15)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() <= self.created_at + timedelta(minutes=5)

    def __str__(self):
        return f"{self.phone} - {self.otp}"


class Forgotpassword(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=6, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()


def generate_server_id():
    today = datetime.now()

    yy = today.strftime("%y")
    mon = today.strftime("%b").upper()
    dd = today.strftime("%d")

    prefix = f"FTW{yy}{mon}{dd}"

    last_user = (
        MyUser.objects
        .filter(server_id__startswith=prefix)
        .order_by("-server_id")
        .first()
    )

    if last_user:
        last_seq = int(last_user.server_id[-2:])
        new_seq = last_seq + 1
    else:
        new_seq = 1

    return prefix + str(new_seq).zfill(2)
