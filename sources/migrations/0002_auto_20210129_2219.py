# Generated by Django 3.1.3 on 2021-01-29 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itarmaterials', '0021_auto_20210129_2202'),
        ('sources', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reference',
            name='itarmaterials',
            field=models.ManyToManyField(blank=True, to='itarmaterials.ITARMaterial'),
        ),
        migrations.AddField(
            model_name='tutorial',
            name='itarmaterials',
            field=models.ManyToManyField(blank=True, to='itarmaterials.ITARMaterial'),
        ),
    ]