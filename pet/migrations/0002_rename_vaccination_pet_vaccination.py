# Generated by Django 5.1.4 on 2025-04-08 22:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pet', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='vaccination',
            new_name='pet_vaccination',
        ),
    ]
