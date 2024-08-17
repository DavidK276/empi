from collections.abc import Sequence

from django.conf import settings
from django.utils import timezone

from emails.models import Email
from research.models import Research, Appointment


class BaseEmail:
    template_name: str
    subject: str

    def __new__(cls, context, **kwargs):
        if cls.template_name is None:
            raise NotImplementedError()
        return Email(template_name=cls.template_name, subject=cls.subject, context=context, **kwargs)


class PublicSignupEmail(BaseEmail):
    template_name = "signup.html"
    subject = "Prihláška na výskum"

    def __new__(cls, participation_nanoid: str, recipients: Sequence[str]):
        signup_link = settings.EMPI_PUBLIC_URL + f"/participation/{participation_nanoid}"
        kwargs = {
            "recipients": recipients,
            "send_when": timezone.now(),
            "is_finalized": True,
        }
        return super().__new__(cls, {"signup_link": signup_link}, **kwargs)


class ResearchCreatedEmail(BaseEmail):
    template_name = "research_created.html"
    subject = "Link na výskum"

    def __new__(cls, research: Research):
        research_admin_url = settings.EMPI_PUBLIC_URL + f"/research/{research.nanoid}/"
        kwargs = {
            "research": research,
            "recipients": research.email_recipients,
            "send_when": timezone.now(),
            "is_finalized": True,
        }
        return super().__new__(cls, {"research_admin_url": research_admin_url}, **kwargs)


class NewSignupEmail(BaseEmail):
    template_name = "signup_created.html"
    subject = "Nové prihlásenie na výskum"

    def __new__(cls, appointment: Appointment):
        research = appointment.research
        kwargs = {
            "research": research,
            "recipients": research.email_recipients,
            "send_when": timezone.now(),
            "is_finalized": True,
        }
        return super().__new__(cls, {"appointment": appointment.serialize()}, **kwargs)


class CancelSignupEmail(BaseEmail):
    template_name = "signup_deleted.html"
    subject = "Prihlásenie na výskum bolo zrušené"

    def __new__(cls, appointment: Appointment):
        research = appointment.research
        kwargs = {
            "research": research,
            "recipients": research.email_recipients,
            "send_when": timezone.now(),
            "is_finalized": True,
        }
        return super().__new__(cls, {"appointment": appointment.serialize()}, **kwargs)


class PasswordResetEmail(BaseEmail):
    template_name = "password_reset.html"
    subject = "Link na obnovu hesla"

    def __new__(cls, passphrase: str, recipients: Sequence[str]):
        password_reset_url = settings.EMPI_PUBLIC_URL + f"/account/password-reset/{passphrase}/"
        kwargs = {
            "recipients": recipients,
            "send_when": timezone.now(),
            "is_finalized": True,
        }
        return super().__new__(cls, {"password_reset_url": password_reset_url}, **kwargs)
