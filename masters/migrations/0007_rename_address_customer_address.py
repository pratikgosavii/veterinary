# Generated by Django 5.1.4 on 2025-04-09 10:15

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0006_event'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='address',
            new_name='customer_address',
        ),
    ]
