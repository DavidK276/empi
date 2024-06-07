import os

from django.contrib.auth.management.commands import createsuperuser


class Command(createsuperuser.Command):
    help = 'Crate a superuser, do nothing if the user already exists'

    def handle(self, *args, **options):
        database = options["database"]
        username = options[self.UserModel.USERNAME_FIELD]
        if username is None:
            username = os.environ.get(
                "DJANGO_SUPERUSER_" + self.UserModel.USERNAME_FIELD.upper(), ""
            )
        if username:
            try:
                self.UserModel._default_manager.db_manager(database).get_by_natural_key(
                    username
                )
            except self.UserModel.DoesNotExist:
                super().handle(*args, **options)
                return
            print("Initial user already exists")
