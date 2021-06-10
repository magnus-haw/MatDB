# Generated by Django 3.2.3 on 2021-06-10 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0002_initial'),
        ('software', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itarexportformat',
            name='material_version',
        ),
        migrations.RemoveField(
            model_name='itarexportformat',
            name='modified_by',
        ),
        migrations.RemoveField(
            model_name='itarexportformat',
            name='software_version',
        ),
        migrations.AddField(
            model_name='softwareversion',
            name='material_properties',
            field=models.ManyToManyField(related_name='materials', to='materials.MaterialProperty'),
        ),
        migrations.DeleteModel(
            name='ExportFormat',
        ),
        migrations.DeleteModel(
            name='ITARExportFormat',
        ),
    ]
