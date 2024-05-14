from typing import TypedDict

from emails.models import Email


class BaseEmail:
    class Context(TypedDict):
        pass

    template_name: str

    def __new__(cls, context: Context, **kwargs):
        if cls.template_name is None:
            raise NotImplementedError()
        return Email(template_name=cls.template_name, context=context, **kwargs)


class PublicSignupEmail(BaseEmail):
    class Context(TypedDict):
        signup_link: str

    template_name = "signup.html"

    def __new__(cls, *args, context: Context, **kwargs):
        return super().__new__(cls, context, **kwargs)
