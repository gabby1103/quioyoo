# Generated by Django 5.1.1 on 2025-01-21 06:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0007_naildesign'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='nail_design',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='appointments.naildesign'),
        ),
        migrations.AlterField(
            model_name='service',
            name='photo',
            field=models.ImageField(blank=True, default='path/to/default/photo.jpg', null=True, upload_to='services/'),
        ),
    ]
