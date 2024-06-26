# Generated by Django 5.0 on 2024-06-27 03:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
        ('passenger', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_id', models.CharField(default='passenger2JANKATXYZ1234', max_length=200, unique=True)),
                ('num_passengers', models.PositiveIntegerField()),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('passenger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='passenger.passenger')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket_id', models.CharField(default='passenger2JANKATXYZ1234', max_length=200, unique=True)),
                ('ticket_file', models.FileField(upload_to='')),
                ('booking', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='organization.booking')),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trip_id', models.CharField(default='JNKKTM', max_length=100, unique=True)),
                ('from_location', models.CharField(max_length=100)),
                ('to_location', models.CharField(max_length=100)),
                ('start_datetime', models.DateTimeField()),
                ('end_datetime', models.DateTimeField()),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_query_name='trip_organization', to='authentication.organization')),
            ],
        ),
        migrations.CreateModel(
            name='TripPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trip_price_id', models.CharField(default='POKKATABC123', max_length=100, unique=True)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.trip')),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='tripprice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.tripprice'),
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_number', models.CharField(default='WXY123ABC', max_length=20, unique=True)),
                ('vehicle_type', models.CharField(choices=[('car', 'Car'), ('van', 'Van'), ('motorcycle', 'Motorcycle')], max_length=10)),
                ('company_made', models.CharField(blank=True, max_length=50)),
                ('model', models.CharField(blank=True, max_length=50)),
                ('age', models.IntegerField(default=18)),
                ('color', models.CharField(default='black', max_length=30)),
                ('seating_capacity', models.PositiveIntegerField(default=0)),
                ('license_plate_number', models.CharField(max_length=10, unique=True)),
                ('insurance_expiry_date', models.DateField(auto_now_add=True)),
                ('fitness_certificate_expiry_date', models.DateField(auto_now_add=True)),
                ('image', models.ImageField(blank=True, upload_to='vehicle_images')),
                ('available_seat', models.PositiveIntegerField(default=0)),
                ('driver', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_query_name='vehicle_driver', to='authentication.driver')),
                ('organization', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_query_name='vehicle_organization', to='authentication.organization')),
            ],
        ),
        migrations.AddField(
            model_name='tripprice',
            name='vehicle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.vehicle'),
        ),
    ]
