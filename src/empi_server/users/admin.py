from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import EmpiUser

admin.site.register(EmpiUser, UserAdmin)
