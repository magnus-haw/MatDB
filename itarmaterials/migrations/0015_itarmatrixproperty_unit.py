# Generated by Django 3.1.3 on 2021-01-21 16:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('units', '0002_combounit_alternate_names'),
        ('itarmaterials', '0014_auto_20210117_2317'),
    ]

    operations = [
        migrations.AddField(
            model_name='itarmatrixproperty',
            name='unit',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='units.combounit'),
        ),
    ]