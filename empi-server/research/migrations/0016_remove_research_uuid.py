# Generated by Django 5.0.5 on 2024-05-08 17:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("research", "0015_auto_20240508_1928"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="research",
            name="uuid",
        ),
    ]