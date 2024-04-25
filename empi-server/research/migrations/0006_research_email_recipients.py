# Generated by Django 5.0.4 on 2024-04-25 07:03

import empi_server.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("research", "0005_auto_20240422_2134"),
    ]

    operations = [
        migrations.AddField(
            model_name="research",
            name="email_recipients",
            field=empi_server.fields.SeparatedValuesField(default="", verbose_name="príjemcovia"),
            preserve_default=False,
        ),
    ]
