from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser

from .utils.validators import validate_acad_year


# Create your models here.


class EmpiUserManager(BaseUserManager):
    def create_user(self, password=""):
        user = self.model()

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, password=""):
        user = self.create_user()
        user.set_password(password)
        user.is_staff = True
        user.save(using=self._db)
        return user


class EmpiUser(AbstractUser):
    password = models.CharField(max_length=128, verbose_name="heslo", blank=False)
    first_name = models.CharField(verbose_name="meno", max_length=150)
    last_name = models.CharField(verbose_name="priezvisko", max_length=150)
    email = models.EmailField()
    REQUIRED_FIELDS = ["first_name", "last_name"]


class Administrator(models.Model):
    user = models.OneToOneField(EmpiUser, on_delete=models.CASCADE)


class Supervisor(models.Model):
    user = models.OneToOneField(EmpiUser, on_delete=models.CASCADE)


class Researcher(models.Model):
    user = models.OneToOneField(EmpiUser, on_delete=models.CASCADE)


class Lecturer(models.Model):
    user = models.OneToOneField(EmpiUser, on_delete=models.CASCADE)


class Participant(models.Model):
    user = models.OneToOneField(EmpiUser, on_delete=models.CASCADE)
    acad_year = models.CharField(verbose_name="akademický rok", max_length=9, blank=False, null=False,
                                 validators=[validate_acad_year])
    chosen_attribute_values = models.ManyToManyField('research.AttributeValue')
