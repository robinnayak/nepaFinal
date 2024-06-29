# Generated by Django 5.0 on 2024-06-29 12:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0003_remove_vehicle_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tripprice',
            name='trip',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='organization.trip'),
        ),
        migrations.AlterField(
            model_name='tripprice',
            name='vehicle',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='organization.vehicle'),
        ),
    ]
