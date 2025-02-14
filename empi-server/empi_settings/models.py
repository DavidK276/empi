from django.db import models


class Settings(models.Model):
    TYPE_CHOICES = (("STR", "String"), ("INT", "Integer"))
    name = models.CharField(blank=False, null=False, unique=True, max_length=128)
    value = models.CharField(max_length=128)
    type = models.CharField(max_length=3, choices=TYPE_CHOICES, default="STR")
