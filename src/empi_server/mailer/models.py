import os

from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Email(models.Model):
    subject = models.CharField(max_length=78, verbose_name="predmet")
    budy = models.TextField()
    send_when = models.DateTimeField(verbose_name="dátum a čas odoslania", blank=True)


class Attachment(models.Model):
    file = models.FileField(upload_to="attachment/")  # TODO: separate into dirs based on year and month
    email = models.ForeignKey(Email, on_delete=models.CASCADE)


@receiver(post_delete, sender=Attachment)
def image_delete(sender, instance, **kwargs):
    os.unlink(instance.image.file.name)
