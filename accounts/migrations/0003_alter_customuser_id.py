# Generated by Django 5.0.6 on 2024-05-31 21:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_customuser_bio_customuser_membership_tier_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
