import base64
import binascii
import re
from typing import Optional

from Crypto.PublicKey import RSA
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _
from rest_framework import authentication, exceptions
from rest_framework.authentication import get_authorization_header

from research.models import Research


class ResearchAuthUser:
    def __init__(self, research=None):
        self.research: Optional[Research] = research

    @property
    def is_authenticated(self):
        return self.research is not None


class ResearchAuthentication(authentication.BasicAuthentication):
    __PATTERN = "^.*([A-Z0-9-]{20}).*$"

    def _get_nanoid_from_path(self, path: str) -> Optional[str]:
        match = re.search(self.__PATTERN, path, re.IGNORECASE)
        if match is None:
            return None
        return match.group(1)

    def _try_unprotected_research_auth(self, request):
        if request is None:
            return None

        nanoid = self._get_nanoid_from_path(request.get_full_path())

        try:
            research = Research.objects.get(nanoid=nanoid)
        except Research.DoesNotExist:
            return None
        if research.is_protected:
            return None

        return ResearchAuthUser(research), None

    def authenticate(self, request):
        """
        Returns a `User` if a correct username and password have been supplied
        using HTTP Basic authentication.  Otherwise returns `None`.
        """
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != b"basic":
            return self._try_unprotected_research_auth(request)

        if len(auth) == 1:
            msg = _("Invalid basic header. No credentials provided.")
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _("Invalid basic header. Credentials string should not contain spaces.")
            raise exceptions.AuthenticationFailed(msg)

        try:
            try:
                auth_decoded = base64.b64decode(auth[1]).decode("utf-8")
            except UnicodeDecodeError:
                auth_decoded = base64.b64decode(auth[1]).decode("latin-1")

            nanoid, password = auth_decoded.split(":", 1)
        except (TypeError, ValueError, UnicodeDecodeError, binascii.Error):
            msg = _("Invalid basic header. Credentials not correctly base64 encoded.")
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(nanoid, password, request)

    def authenticate_credentials(self, nanoid, password, request: Optional[HttpRequest] = None):
        if request is None:
            return None

        try:
            research = Research.objects.get(nanoid=nanoid)
        except Research.DoesNotExist:
            return None
        if research.is_protected:
            try:
                _ = RSA.import_key(research.privkey, password)
            except (ValueError, IndexError, TypeError):
                raise exceptions.AuthenticationFailed()

        return ResearchAuthUser(research), None
