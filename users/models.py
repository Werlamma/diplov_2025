from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    patronymic = models.CharField(max_length=30, blank=True, null=True, verbose_name="Отчество")
    phone_number = models.CharField(max_length=18, verbose_name="Номер телефона")



