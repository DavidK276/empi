from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from .models import EmpiUser, Attribute, AttributeValue, Participant
from django.utils.translation import gettext_lazy as _


class EmpiUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("password",)}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("usable_password", "password1", "password2"),
            },
        ),
    )
    list_display = ("email", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("first_name", "last_name", "email")
    ordering = ("email",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )


admin.site.register(EmpiUser, EmpiUserAdmin)

admin.site.register(Attribute, ModelAdmin)

admin.site.register(AttributeValue, ModelAdmin)

admin.site.register(Participant, ModelAdmin)
