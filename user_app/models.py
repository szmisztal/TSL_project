from django.db import models
from django.contrib.auth.models import AbstractUser

class UserRole(models.TextChoices):
    LOGISTICIAN = "Logistician"
    DISPATCHER = "Dispatcher"
    DRIVER = "Driver"

class CustomUser(AbstractUser):
    username = models.CharField(max_length = 32, unique = True)
    first_name = models.CharField(max_length = 16)
    last_name = models.CharField(max_length = 16)
    email = models.EmailField(blank = True, null = True)
    phone_number = models.PositiveSmallIntegerField(blank = True, null = True)
    role = models.CharField(max_length = 16, choices = UserRole.choices)
