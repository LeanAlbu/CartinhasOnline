from enum import unique

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email = email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, password, **extra_fields)

    def get_by_natural_key(self, username):
        email=self.normalize_email(username)
        return self.get(**{self.model.USERNAME_FIELD:email})

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique = True)
    elo = models.IntegerField(default = 500)
    is_staff = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    date_joined = models.DateField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Match(models.Model):
    winner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name = 'matches_won')
    loser = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name = 'matches_loser')
    match_date = models.DateTimeField(auto_now_add=True)
