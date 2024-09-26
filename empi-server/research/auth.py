import re
from typing import Optional

from typing_extensions import override

from Crypto.PublicKey import RSA
from django.http import HttpRequest
from rest_framework import authentication, exceptions

from research.models import Research


class ResearchAuthUser:
    def __init__(self, research=None):
        self.research: Optional[Research] = research


class ResearchAuthentication(authentication.BasicAuthentication):
    __PATTERN = "^.*([A-Z0-9-]{20}).*$"

    def _get_nanoid_from_path(self, path: str) -> Optional[str]:
        match = re.search(self.__PATTERN, path, re.IGNORECASE)
        if match is None:
            return None
        return match.group(1)

    @override
    # overriding this method is necessary to authenticate unprotected research
    # when the request doesn't contain the Authorization header
    def authenticate(self, request):
        if request is None:
            return None

        nanoid = self._get_nanoid_from_path(request.get_full_path())

        try:
            research = Research.objects.get(nanoid=nanoid)
        except Research.DoesNotExist:
            return None
        if research.is_protected:
            return super().authenticate(request)

        return ResearchAuthUser(research), None

    @override
    def authenticate_credentials(self, userid, password, request: Optional[HttpRequest] = None):
        if request is None:
            return None

        nanoid = self._get_nanoid_from_path(request.get_full_path())

        try:
            research = Research.objects.get(nanoid=nanoid)
        except Research.DoesNotExist:
            return None
        if research.is_protected:
            _, privkey = research.get_keypair()
            try:
                RSA.import_key(privkey, password)
            except (ValueError, IndexError, TypeError):
                raise exceptions.AuthenticationFailed()

        return ResearchAuthUser(research), None
