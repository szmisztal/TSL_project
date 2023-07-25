from django.db import models

class CurrentOrderManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(done = False)

class ArchivedOrderManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(done = True)

