# Generated by Django 5.1.4 on 2025-04-06 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('serviceprovider', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service_provider',
            name='mobile_no',
        ),
    ]
