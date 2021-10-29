from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.
class AccountManager(BaseUserManager):

    def create_user(self, username, password):
        if not username:
            raise ValueError('The given username must be set')

        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username=username, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    username = models.CharField(verbose_name="Username", max_length=15, blank=False, unique=True)
    is_superuser = models.BooleanField(default=False, blank=False)
    is_staff = models.BooleanField(default=False, blank=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    date_joined = models.DateTimeField(verbose_name="Date Joined", auto_now_add=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = AccountManager()

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.username

    def check_superuser(self):
        return self.is_superuser

    def check_staff(self):
        return self.is_staff

    def check_student(self):
        return not self.is_staff


# proxy model for Account model(Custom User Model)
class Student(Account):
    class Meta:
        proxy = True

    def __str__(self):
        return self.username
