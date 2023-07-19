from django.db import models

class DriverManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(role = "Driver")
