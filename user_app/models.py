from django.db import models
from django.contrib.auth.models import AbstractUser, Group, UserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from .managers import DriverManager

class UserRole(models.TextChoices):
    LOGISTICIAN = "Logistician"
    DISPATCHER = "Dispatcher"
    DRIVER = "Driver"

class LogisticiansGroup(Group):
    name = "Logisticians group"

    def __str__(self):
        return self.name

class DispatchersGroup(Group):
    name = "Dispatchers group"

    def __str__(self):
        return self.name

class DriversGroup(Group):
    name = "Drivers group"

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    username = models.CharField(max_length = 32, unique = True)
    first_name = models.CharField(max_length = 16)
    last_name = models.CharField(max_length = 16)
    email = models.EmailField(blank = True, null = True, unique = True)
    phone_number = models.PositiveSmallIntegerField(unique = True)
    role = models.CharField(max_length = 16, choices = UserRole.choices)

    objects = UserManager()
    drivers = DriverManager()

    def set_group(self):
        group = None
        if self.role == UserRole.LOGISTICIAN:
            group = Group.objects.get(name = "Logisticians group")
        if self.role == UserRole.DISPATCHER:
            group = Group.objects.get(name = "Dispatchers group")
        if self.role == UserRole.DRIVER:
            group = Group.objects.get(name = "Drivers group")

        if group:
            self.groups.add(group)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.role}, phone: {self.phone_number}, mail: {self.email}"

@receiver(post_save, sender = CustomUser)
def create_auth_token(sender, instance = None, created = False, **kwargs):
    if created:
        Token.objects.create(user = instance)
