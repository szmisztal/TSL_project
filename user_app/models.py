from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserRole(models.TextChoices):
    LOGISTICIAN = "Logistician"
    DISPATCHER = "Dispatcher"
    DRIVER = "Driver"

class CustomUser(AbstractUser):
    username = models.CharField(max_length = 32, unique = True)
    first_name = models.CharField(max_length = 16)
    last_name = models.CharField(max_length = 16)
    email = models.EmailField(blank = True, null = True, unique = True)
    phone_number = models.PositiveSmallIntegerField(unique = True)
    role = models.CharField(max_length = 16, choices = UserRole.choices)

    def set_group(self):
        if self.role == UserRole.LOGISTICIAN:
            group = LogisticianGroup.objects.get(name = "Logistician group")
        elif self.role == UserRole.DISPATCHER:
            group = DispatcherGroup.objects.get(name = "Dispatcher group")
        elif self.role == UserRole.DRIVER:
            group = DriverGroup.objects.get(name = "Driver group")
        else:
            group = None

        if group:
            self.groups.add(group)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.role}, phone: {self.phone_number}, mail: {self.email}"

@receiver(post_save, sender = CustomUser)
def create_auth_token(sender, instance = None, created = False, **kwargs):
    if created:
        Token.objects.create(user = instance)

class LogisticianGroup(Group):
    name = "Logisticians group"

    def __str__(self):
        return {self.name}

class DispatcherGroup(Group):
    name = "Dispatchers group"

    def __str__(self):
        return {self.name}

class DriverGroup(Group):
    name = "Drivers group"

    def __str__(self):
        return {self.name}
