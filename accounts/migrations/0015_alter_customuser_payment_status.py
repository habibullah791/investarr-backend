# Generated by Django 5.0.6 on 2024-07-08 01:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0014_customuser_payment_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="payment_status",
            field=models.CharField(
                blank=True,
                choices=[("Pending", "Pending"), ("Success", "Success")],
                default="Pending",
                max_length=255,
                null=True,
            ),
        ),
    ]
