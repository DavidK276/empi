import os

from datetime import datetime
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .fields import SeparatedValuesField


class Email(models.Model):
    recipients = SeparatedValuesField(verbose_name="príjemcovia", field=models.EmailField)
    subject = models.CharField(max_length=78, verbose_name="predmet")
    body = models.TextField(verbose_name="telo")
    send_when = models.DateTimeField(verbose_name="dátum a čas odoslania", blank=True)


class Attachment(models.Model):
    file = models.FileField(verbose_name="súbor", upload_to="attachment/")
    email = models.ForeignKey(Email, on_delete=models.CASCADE)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        now = datetime.now()
        year, month = now.year, now.month
        directory = self.file.file.name.parent
        destination = directory / str(year) / str(month)
        self.file.file.name = destination
        super().save(force_insert, force_update, using, update_fields)


@receiver(post_delete, sender=Attachment)
def attachment_delete(sender, instance, **kwargs):
    os.unlink(instance.file.file.name)
