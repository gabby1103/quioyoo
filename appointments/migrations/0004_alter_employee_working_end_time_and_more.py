# Generated by Django 5.1.1 on 2024-12-20 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0003_alter_employee_name_alter_employee_phone_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='working_end_time',
            field=models.TimeField(default='17:00'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='working_start_time',
            field=models.TimeField(default='09:00'),
        ),
        migrations.AlterField(
            model_name='service',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='service/'),
        ),
    ]
