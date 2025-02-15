from django.contrib import admin
from django.contrib.admin import ModelAdmin

from empi_settings.models import Settings

admin.site.register(Settings, ModelAdmin)
