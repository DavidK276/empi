# Generated by Django 5.0.4 on 2024-04-22 19:34

import uuid

from django.db import migrations


def gen_uuid(apps, schema_editor):
    Model = apps.get_model("research", "Participation")
    for row in Model.objects.all():
        row.uuid = uuid.uuid4()
        row.save(update_fields=["uuid"])


class Migration(migrations.Migration):
    dependencies = [
        ("research", "0003_rename_protected_research_is_protected_and_more"),
    ]

    operations = [
        migrations.RunPython(gen_uuid, reverse_code=migrations.RunPython.noop),
    ]
