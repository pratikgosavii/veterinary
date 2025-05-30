# Generated by Django 5.1.4 on 2025-04-12 10:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('pet', '0010_test_booking_report'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cart',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='cart',
            name='content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='cart',
            name='object_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='cart',
            name='product',
        ),
    ]
