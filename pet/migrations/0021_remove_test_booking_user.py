# Generated by Django 5.1.4 on 2025-04-18 09:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pet', '0020_remove_onlineconsultationappointmentreport_appointment_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test_booking',
            name='user',
        ),
    ]
