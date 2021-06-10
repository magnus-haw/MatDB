# Generated by Django 3.2.3 on 2021-06-10 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0002_initial'),
        ('software', '0003_auto_20210610_0109'),
    ]

    operations = [
        migrations.AddField(
            model_name='softwareversion',
            name='can_export',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='softwareversion',
            name='material_properties',
            field=models.ManyToManyField(related_name='software_versions', to='materials.MaterialProperty'),
        ),
    ]
