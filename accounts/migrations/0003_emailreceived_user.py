# Generated by Django 4.2.14 on 2024-07-16 21:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_emailreceived_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailreceived',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
