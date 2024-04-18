# Generated by Django 5.0.3 on 2024-04-18 09:17

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
            model_name="research",
            name="chosen_attribute_values",
            field=models.ManyToManyField(blank=True, to="users.attributevalue"),
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
                    ("info_url__isnull", True),
                    ("location__isnull", True),
                    _connector="XOR",
                ),
                name="one_of_url_location_null",
            ),
        ),
    ]
