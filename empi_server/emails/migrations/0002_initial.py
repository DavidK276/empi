# Generated by Django 5.0.3 on 2024-03-05 15:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("emails", "0001_initial"),
        ("research", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="email",
            name="research",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="research.research"
            ),
        ),
        migrations.AddField(
            model_name="attachment",
            name="email",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="emails.email"
            ),
        ),
    ]
