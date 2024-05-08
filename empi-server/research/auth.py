import re
from typing import Optional

from Crypto.PublicKey import RSA
from django.http import HttpRequest
from rest_framework import authentication, exceptions

from research.models import Research


class ResearchAuthUser:
    def __init__(self, research=None):
        self.research: Optional[Research] = research


class ResearchAuthentication(authentication.BasicAuthentication):

    def authenticate_credentials(self, userid, password, request: Optional[HttpRequest] = None):
        if request is None:
            return None

        path = request.get_full_path()
        pattern = "^.*([A-Z0-9-]{20}).*$"
        match = re.search(pattern, path, re.IGNORECASE)
        if match is None:
            return None
        nanoid = match.group(1)

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
