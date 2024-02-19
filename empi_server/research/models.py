from django.db import models


class Credit(models.Model):
    value = models.PositiveIntegerField(verbose_name="hodnota")
    research = models.CharField(max_length=200, blank=True)
    participant = models.ForeignKey('users.Participant', on_delete=models.CASCADE)


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


class Research(models.Model):
    url = models.URLField()


class Appointment(models.Model):
    when = models.DateTimeField(verbose_name="kedy", blank=False)
    capacity = models.IntegerField(verbose_name="kapacita")
    research = models.ForeignKey(Research, on_delete=models.CASCADE)
    comment = models.TextField(blank=True)


class InPersonAppointment(models.Model):
    location = models.TextField(blank=False)


class OnlineAppointment(models.Model):
    url = models.URLField()
