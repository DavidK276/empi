import zoneinfo
from collections.abc import Sequence
from datetime import datetime
from typing import TypedDict

from django.conf import settings

from emails.models import Email


class BaseEmail:
    template_name: str

    def __new__(cls, context, **kwargs):
        if cls.template_name is None:
            raise NotImplementedError()
        return Email(template_name=cls.template_name, context=context, **kwargs)


class PublicSignupEmail(BaseEmail):
    class Context(TypedDict):
        signup_link: str

    template_name = "signup.html"
    subject = "Prihláška na výskum"

    def __new__(cls, signup_link: str, recipients: Sequence[str]):
        kwargs = {
            "recipients": recipients,
            "subject": cls.subject,
            "send_when": datetime.now(tz=zoneinfo.ZoneInfo(settings.TIME_ZONE)),
            "is_finalized": True,
        }
        return super().__new__(cls, {"signup_link": signup_link}, **kwargs)
