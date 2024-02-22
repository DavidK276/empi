from django.db import models
from django.db.models import Q

from .utils.constants import *


class Research(models.Model):
    name = models.CharField(max_length=120, verbose_name="meno")
    url = models.URLField()
    points = models.PositiveIntegerField(verbose_name="body")


class Credit(models.Model):
    research = models.ForeignKey(Research, on_delete=models.CASCADE)
    participant_token_encrypted = models.BinaryField()


class Attribute(models.Model):
    class AttributeType(models.TextChoices):
        SINGLE_CHOICE = 'SC', 'Výber jednej hodnoty'
        MULTIPLE_CHOICE = 'MC', 'Výber viacero hodnôt'
        ENTER_TEXT = 'ET', 'Výpis textu'

    name = models.CharField(max_length=150, blank=False)
    type = models.CharField(max_length=2, choices=AttributeType.choices, default=AttributeType.SINGLE_CHOICE)


class AttributeValue(models.Model):
    name = models.CharField(max_length=150, blank=False)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)


class Appointment(models.Model):
    research = models.ForeignKey(Research, on_delete=models.CASCADE)
    when = models.DateTimeField(verbose_name="kedy", blank=False)
    capacity = models.IntegerField(verbose_name="kapacita")
    comment = models.TextField(blank=True)
    location = models.TextField(blank=False, null=True)
    url = models.URLField(blank=False, null=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=Q(url__isnull=True) ^ Q(location__isnull=True),
                                   name="one_of_url_location_null")
        ]

    def get_type(self):
        if self.location is None:
            return AppointmentType.ONLINE
        return AppointmentType.IN_PERSON


class Participation(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    participant_token_encrypted = models.BinaryField()
