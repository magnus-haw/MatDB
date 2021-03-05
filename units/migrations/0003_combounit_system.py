# Generated by Django 3.1.3 on 2021-03-05 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('units', '0002_combounit_alternate_names'),
    ]

    operations = [
        migrations.AddField(
            model_name='combounit',
            name='system',
            field=models.PositiveIntegerField(choices=[(0, 'SI'), (1, 'Imperial')], default=0),
        ),
    ]
