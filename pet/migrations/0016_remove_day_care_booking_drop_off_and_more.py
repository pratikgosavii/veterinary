# Generated by Django 5.1.4 on 2025-04-15 10:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pet', '0015_rename_half_day_on_checkin_day_care_booking_full_day_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='day_care_booking',
            name='drop_off',
        ),
        migrations.RemoveField(
            model_name='day_care_booking',
            name='pick_up',
        ),
    ]
