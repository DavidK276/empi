# Generated by Django 5.0.3 on 2024-04-18 09:17

import emails.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Attachment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "file",
                    models.FileField(upload_to="attachment/", verbose_name="súbor"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Email",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "recipients",
                    emails.fields.SeparatedValuesField(verbose_name="príjemcovia"),
                ),
                ("subject", models.CharField(max_length=78, verbose_name="predmet")),
                ("body", models.TextField(verbose_name="telo")),
                (
                    "send_when",
                    models.DateTimeField(blank=True, null=True, verbose_name="dátum a čas odoslania"),
                ),
                (
                    "is_finalized",
                    models.BooleanField(default=False, verbose_name="je publikovaný"),
                ),
            ],
        ),
    ]
