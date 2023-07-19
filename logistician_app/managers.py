from django.db import models

class DriverIsNullManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(driver__isnull = True)
