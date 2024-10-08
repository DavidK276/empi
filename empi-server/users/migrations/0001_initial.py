# Generated by Django 5.0.6 on 2024-08-17 09:41

import django.db.models.deletion
import django.utils.timezone
import users.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Attribute",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150, unique=True)),
                (
                    "type",
                    models.CharField(
                        choices=[("SC", "Výber jednej hodnoty"), ("MC", "Výber viacero hodnôt"), ("ET", "Vpis textu")],
                        default="SC",
                        max_length=2,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="BackupKey",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nonce", models.BinaryField(max_length=16)),
                ("tag", models.BinaryField(max_length=16)),
                ("backup_key", models.BinaryField(max_length=4096)),
            ],
        ),
        migrations.CreateModel(
            name="AttributeValue",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("value", models.CharField(max_length=150, verbose_name="hodnota")),
                (
                    "attribute",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="values",
                        to="users.attribute",
                        verbose_name="atribút",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EmpiUser",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("last_login", models.DateTimeField(blank=True, null=True, verbose_name="last login")),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                ("first_name", models.CharField(blank=True, max_length=150, verbose_name="first name")),
                ("last_name", models.CharField(blank=True, max_length=150, verbose_name="last name")),
                ("email", models.EmailField(blank=True, max_length=254, unique=True, verbose_name="email address")),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                ("date_joined", models.DateTimeField(default=django.utils.timezone.now, verbose_name="date joined")),
                ("pubkey", models.BinaryField(max_length=1024)),
                ("privkey", models.BinaryField(max_length=4096)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
                (
                    "backup_privkey",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="users.backupkey"),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "default_manager_name": "users",
            },
            managers=[
                ("users", users.models.EmpiUserManager()),
            ],
        ),
        migrations.CreateModel(
            name="EncryptedSessionKey",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("data", models.BinaryField(max_length=1024)),
                ("admin", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ("backup_key", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="users.backupkey")),
            ],
        ),
        migrations.CreateModel(
            name="ResetKey",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("valid_until", models.DateTimeField()),
                ("backup_key", models.BinaryField(max_length=4096)),
                (
                    "user",
                    models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Participant",
            fields=[
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "acad_year",
                    models.CharField(
                        default=users.models.generate_acad_year, max_length=7, verbose_name="akademický rok"
                    ),
                ),
                (
                    "token",
                    models.CharField(default=users.models.generate_token, editable=False, max_length=9, unique=True),
                ),
                (
                    "chosen_attribute_values",
                    models.ManyToManyField(blank=True, related_name="attributes", to="users.attributevalue"),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="attributevalue",
            constraint=models.UniqueConstraint(
                models.F("attribute"), models.F("value"), name="unique_value_per_attribute"
            ),
        ),
    ]
