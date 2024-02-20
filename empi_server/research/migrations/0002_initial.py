# Generated by Django 5.0.2 on 2024-02-20 11:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("research", "0001_initial"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="credit",
            name="participant",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="users.participant"
            ),
        ),
        migrations.AddField(
            model_name="appointment",
            name="research",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="research.research"
            ),
        ),
    ]
