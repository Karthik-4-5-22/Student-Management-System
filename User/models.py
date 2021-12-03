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





class Courses(models.Model):
    name = models.CharField(verbose_name="Course Name", max_length=60, blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name="Course"
        verbose_name_plural="Courses"


class Details(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    firstname = models.CharField(verbose_name="First Name", max_length=20, blank=False)
    lastname = models.CharField(verbose_name="Last Name", max_length=20)
    email = models.CharField(verbose_name="Email", max_length=60, blank=False)
    mobile_no = models.CharField(verbose_name="Mobile Number", max_length=10, blank=False)
    course = models.ForeignKey(Courses, on_delete=models.PROTECT)
    current_year=models.IntegerField(verbose_name="Year",max_length=1,editable=False,default=1)
    cgpa = models.FloatField(verbose_name="CGPA", max_length=3)


    class Meta:
        verbose_name="Details"
        verbose_name_plural="Details"


    def __str__(self):
        return self.firstname

# proxy model for Account model(Custom User Model)
class Student(Account):
    class Meta:
        proxy = True

    def __str__(self):
        return self.username