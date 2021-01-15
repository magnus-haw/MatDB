# Generated by Django 3.1.3 on 2021-01-14 17:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import materials.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('units', '0002_combounit_alternate_names'),
        ('materials', '0022_delete_variableproperties'),
        ('itarmaterials', '0010_auto_20210114_0004'),
    ]

    operations = [
        migrations.CreateModel(
            name='ITARVariableProperty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('state', models.PositiveIntegerField(choices=[(0, 'Virgin'), (1, 'Char'), (2, 'Pyrolysis')], default=0, verbose_name='Material state')),
                ('p', materials.models.MyArrayField(blank=True, null=True, verbose_name='Pressure [Pa]')),
                ('T', materials.models.MyArrayField(blank=True, null=True, verbose_name='Temperature [K]')),
                ('values', materials.models.MyArrayField(blank=True, null=True)),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='itarmaterials.itarmaterialversion')),
                ('material_version', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materials.materialversion')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('unit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='units.combounit')),
            ],
            options={
                'verbose_name_plural': 'ITAR Variable properties',
            },
        ),
        migrations.DeleteModel(
            name='ITARVariableProperties',
        ),
    ]
