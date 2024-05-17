# Generated by Django 5.0.5 on 2024-05-14 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("emails", "0003_email_is_sent"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="email",
            name="body",
        ),
        migrations.AddField(
            model_name="email",
            name="context",
            field=models.JSONField(default="", verbose_name="kontextové dáta"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="email",
            name="template_name",
            field=models.CharField(default="", max_length=255, verbose_name="šablóna"),
            preserve_default=False,
        ),
    ]