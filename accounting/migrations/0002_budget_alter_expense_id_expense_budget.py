# Generated by Django 4.1 on 2022-09-20 21:15

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounting", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Budget",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        default="Budget-09/20/2022-21:15:57",
                        max_length=255,
                        unique=True,
                    ),
                ),
            ],
        ),
        migrations.AlterField(
            model_name="expense",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False
            ),
        ),
        migrations.AddField(
            model_name="expense",
            name="budget",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="accounting.budget",
            ),
        ),
    ]