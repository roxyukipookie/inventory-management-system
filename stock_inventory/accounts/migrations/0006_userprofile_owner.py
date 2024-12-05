# Generated by Django 5.1.1 on 2024-11-29 16:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_customuser_is_owner_customuser_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='staff', to=settings.AUTH_USER_MODEL),
        ),
    ]