# Generated by Django 3.1.3 on 2021-01-22 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itarmaterials', '0014_auto_20210117_2317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itarmaterialversion',
            name='version',
            field=models.CharField(max_length=25),
        ),
    ]