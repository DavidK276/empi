# Generated by Django 5.0.6 on 2024-06-12 14:30

import empi_server.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='attachment/', verbose_name='súbor')),
            ],
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipients', empi_server.fields.SeparatedValuesField(verbose_name='príjemcovia')),
                ('subject', models.CharField(max_length=78, verbose_name='predmet')),
                ('template_name', models.CharField(max_length=255, verbose_name='šablóna')),
                ('context', models.JSONField(verbose_name='kontextové dáta')),
                ('send_when', models.DateTimeField(verbose_name='dátum a čas odoslania')),
                ('is_finalized', models.BooleanField(default=False, verbose_name='je publikovaný')),
                ('is_sent', models.BooleanField(default=False, editable=False, verbose_name='odoslaný')),
            ],
        ),
    ]
