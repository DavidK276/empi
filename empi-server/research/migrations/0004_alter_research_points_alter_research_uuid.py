# Generated by Django 5.0.3 on 2024-04-16 08:49

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("research", "0003_research_is_published_research_protected_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="research",
            name="points",
            field=models.PositiveIntegerField(
                blank=True, null=True, verbose_name="body"
            ),
        ),
        migrations.AlterField(
            model_name="research",
            name="uuid",
            field=models.UUIDField(
                default=uuid.UUID("28ff81d5-3c42-42ba-8c29-d41790a883cc"),
                editable=False,
                primary_key=True,
                serialize=False,
            ),
        ),
    ]
