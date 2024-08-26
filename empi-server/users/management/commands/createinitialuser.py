import os

from django.contrib.auth.management.commands import createsuperuser

from users.models import EmpiUser


class Command(createsuperuser.Command):
    help = "Crate a superuser, do nothing if the user already exists"

    def handle(self, *args, **options):
        database = options["database"]
        username = options[EmpiUser.USERNAME_FIELD]
        if username is None:
            username = os.environ.get("DJANGO_SUPERUSER_" + EmpiUser.USERNAME_FIELD.upper(), "")
        if username:
            try:
                EmpiUser.users.db_manager(database).get_by_natural_key(username)
            except EmpiUser.DoesNotExist:
                super().handle(*args, **options)
                return
            print("Initial user already exists")
