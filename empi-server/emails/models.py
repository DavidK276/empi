import os
from collections.abc import Sequence
from datetime import datetime
from email.mime.application import MIMEApplication
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from typing import Optional

import magic
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.template.loader import render_to_string
from empi_server.fields import SeparatedValuesField
from research import models as research_models
from html2text import html2text


class Email(models.Model):
    research = models.ForeignKey(research_models.Research, on_delete=models.CASCADE, blank=True, null=True)
    recipients = SeparatedValuesField(verbose_name="príjemcovia", field=models.EmailField)
    subject = models.CharField(max_length=78, verbose_name="predmet")
    template_name = models.CharField(max_length=255, verbose_name="šablóna")
    context = models.JSONField(verbose_name="kontextové dáta")
    send_when = models.DateTimeField(verbose_name="dátum a čas odoslania")
    is_finalized = models.BooleanField(verbose_name="je publikovaný", default=False)
    is_sent = models.BooleanField(verbose_name="odoslaný", default=False, editable=False)

    @classmethod
    def get_emails_to_send(cls):
        return cls.objects.filter(is_sent=False).filter(
            (Q(send_when__isnull=True) | Q(send_when__lte=datetime.now())) & Q(is_finalized=True)
        )

    def _get_context(self):
        if self.research is None:
            return self.context
        return self.context | {"research": self.research.serialize()}

    def send(self, recipients: Optional[Sequence[str]] = None):
        html = render_to_string(self.template_name, context=self._get_context())
        text = html2text(html)
        attachments = [attachment.get_mimebase() for attachment in Attachment.objects.filter(email=self.pk)]

        message = EmailMultiAlternatives(
            subject=self.subject,
            body=text,
            from_email=settings.EMPI_FROM_EMAIL,
            to=[],
            bcc=recipients or self.recipients,
            connection=None,
            attachments=attachments,
            headers={},
            cc=[],
            reply_to=settings.EMPI_REPLY_TO_EMAILS,
        )
        message.attach_alternative(html, "text/html")
        message.send()

        self.is_sent = True
        if self.pk is not None:
            self.save(update_fields=["is_sent"])
        else:
            self.save()


class Attachment(models.Model):
    file = models.FileField(verbose_name="súbor", upload_to="attachment/")
    email = models.ForeignKey(Email, on_delete=models.CASCADE)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        now = datetime.now()
        year, month = now.year, now.month
        directory = self.file.file.value.parent
        destination = directory / str(year) / str(month)
        self.file.file.value = destination
        super().save(force_insert, force_update, using, update_fields)

    def get_mimebase(self):
        maintype, subtype = magic.from_file(self.file.path, mime=True).split("/", maxsplit=1)
        mode = "r" if maintype == "text" else "rb"
        with self.file.open(mode) as f:
            data = f.read()
            if maintype == "application":
                return MIMEApplication(data, subtype)
            elif maintype == "audio":
                return MIMEAudio(data, subtype)
            elif maintype == "image":
                return MIMEImage(data, subtype)
            elif maintype == "text":
                return MIMEText(data, subtype)


@receiver(post_delete, sender=Attachment)
def attachment_delete(_sender, instance, **_kwargs):
    os.unlink(instance.file.file.value)
