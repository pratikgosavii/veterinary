# Generated by Django 5.1.4 on 2025-04-16 22:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0020_consultation_type_online_consultation_type'),
        ('pet', '0017_remove_consultation_appointment_is_online_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='object_id',
        ),
        migrations.RemoveField(
            model_name='order_item',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='order_item',
            name='object_id',
        ),
        migrations.AddField(
            model_name='cart',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='masters.product'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order_item',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='masters.product'),
            preserve_default=False,
        ),
    ]
