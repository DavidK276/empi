from django.core.management import BaseCommand

from emails import models


class Command(BaseCommand):
    help = "Sends all emails scheduled for sending"

    def handle(self, *args, **options):
        emails = models.Email.get_emails_to_send()
        for email in emails:
            email.send()
