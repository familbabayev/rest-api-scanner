from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from django.db.models.signals import pre_delete
from django.dispatch import receiver
import os


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Collection(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )
    title = models.CharField(max_length=150)
    file = models.FileField(upload_to='')


class Vulnerability(models.Model):
    title = models.CharField(max_length=255)
    recommendation = models.TextField()
    severity = models.CharField(max_length=150)


class Scan(models.Model):
    vulnerabilities = models.ManyToManyField(
        Vulnerability, through='ScanDetail'
    )
    scan_date = models.DateTimeField(auto_now_add=True)
    scan_type = models.CharField(max_length=150)
    coll_title = models.CharField(max_length=255)
    status = models.CharField(max_length=150, default="RUNNING")
    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE
    )


class ScanDetail(models.Model):
    vulnerability = models.ForeignKey(
        Vulnerability, null=True, blank=True, on_delete=models.CASCADE
    )
    scan = models.ForeignKey(
        Scan, null=True, blank=True, on_delete=models.CASCADE
    )


@receiver(pre_delete, sender=Collection)
def delete_file(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
