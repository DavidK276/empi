import os
import magic

from datetime import datetime

from django.db.models import Q
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from .fields import SeparatedValuesField


class Email(models.Model):
    recipients = SeparatedValuesField(verbose_name="príjemcovia", field=models.EmailField)
    subject = models.CharField(max_length=78, verbose_name="predmet")
    body = models.TextField(verbose_name="telo")
    send_when = models.DateTimeField(verbose_name="dátum a čas odoslania", blank=True, null=True)
    is_finalized = models.BooleanField(verbose_name="je publikovaný", null=False, default=False)

    @classmethod
    def get_emails_to_send(cls):
        return cls.objects.filter(Q(send_when__isnull=True) | Q(send_when__lte=datetime.now()))

    def send(self):
        html = render_to_string('email.html', context={'subject': self.subject, 'body': self.body})
        attachments = [attachment.get_mimebase() for attachment in Attachment.objects.filter(email=self.pk)]

        message = EmailMultiAlternatives(subject=self.subject,
                                         body=self.body,
                                         from_email='noreply@example.com',
                                         to=[],
                                         bcc=self.recipients,
                                         connection=None,
                                         attachments=attachments,
                                         headers={},
                                         cc=[],
                                         reply_to='admin@example.com')
        message.attach_alternative(html, 'text/html')
        message.send()


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

    def get_mimebase(self):
        maintype, subtype = magic.from_file(self.file.path, mime=True).split('/', maxsplit=1)
        mode = 'r' if maintype == 'text' else 'rb'
        with self.file.open(mode) as f:
            data = f.read()
            if maintype == 'application':
                return MIMEApplication(data, subtype)
            elif maintype == 'audio':
                return MIMEAudio(data, subtype)
            elif maintype == 'image':
                return MIMEImage(data, subtype)
            elif maintype == 'text':
                return MIMEText(data, subtype)


@receiver(post_delete, sender=Attachment)
def attachment_delete(sender, instance, **kwargs):
    os.unlink(instance.file.file.name)
