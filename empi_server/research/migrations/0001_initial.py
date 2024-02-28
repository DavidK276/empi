# Generated by Django 5.0.2 on 2024-02-28 14:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Appointment",
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
                ("when", models.DateTimeField(verbose_name="kedy")),
                ("capacity", models.IntegerField(verbose_name="kapacita")),
                ("comment", models.TextField(blank=True)),
                ("location", models.TextField(null=True)),
                ("url", models.URLField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Research",
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
                    "name",
                    models.CharField(max_length=120, unique=True, verbose_name="meno"),
                ),
                ("url", models.URLField()),
                ("points", models.PositiveIntegerField(verbose_name="body")),
                ("created", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Participation",
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
                    "recipient_type",
                    models.CharField(
                        choices=[
                            ("LE", "vyučujúci"),
                            ("ST", "študent"),
                            ("EX", "expert"),
                        ],
                        max_length=2,
                        verbose_name="typ príjemcu",
                    ),
                ),
                ("participant_token_encrypted", models.BinaryField()),
                (
                    "appointment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="research.appointment",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Credit",
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
                    "recipient_type",
                    models.CharField(
                        choices=[
                            ("LE", "vyučujúci"),
                            ("ST", "študent"),
                            ("EX", "expert"),
                        ],
                        max_length=2,
                        verbose_name="typ príjemcu",
                    ),
                ),
                ("participant_token_encrypted", models.BinaryField()),
                (
                    "research",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="research.research",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="appointment",
            name="research",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="research.research"
            ),
        ),
        migrations.AddConstraint(
            model_name="appointment",
            constraint=models.CheckConstraint(
                check=models.Q(
                    ("url__isnull", True), ("location__isnull", True), _connector="XOR"
                ),
                name="one_of_url_location_null",
            ),
        ),
    ]
