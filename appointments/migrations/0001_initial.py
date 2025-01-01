# Generated by Django 5.1.1 on 2024-12-19 09:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=15)),
                ('bio', models.TextField()),
                ('photo', models.ImageField(blank=True, null=True, upload_to='employee_photos/')),
                ('working_start_time', models.TimeField(default='09:00')),
                ('working_end_time', models.TimeField(default='17:00')),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=255)),
                ('customer_phone', models.CharField(max_length=15)),
                ('appointment_time', models.DateTimeField()),
                ('status', models.CharField(choices=[('Scheduled', 'Scheduled'), ('Completed', 'Completed'), ('Canceled', 'Canceled')], default='Scheduled', max_length=20)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appointments.employee')),
            ],
        ),
    ]
