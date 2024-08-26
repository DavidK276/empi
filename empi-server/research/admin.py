from django.contrib import admin
from django.contrib.admin import ModelAdmin

from research.models import Research, Appointment, Participation

# Register your models here.

admin.site.register(Research, ModelAdmin)

admin.site.register(Appointment, ModelAdmin)

admin.site.register(Participation, ModelAdmin)
