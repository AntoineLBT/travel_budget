# Generated by Django 4.2.1 on 2024-03-24 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounting", "0014_alter_trip_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="expense",
            name="amount",
            field=models.DecimalField(decimal_places=2, max_digits=20),
        ),
    ]