# Generated by Django 5.0.2 on 2024-03-05 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_alter_participant_chosen_attribute_values"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="attributevalue",
            constraint=models.UniqueConstraint(
                models.F("attribute"),
                models.F("value"),
                name="unique_value_per_attribute",
            ),
        ),
    ]
