# Generated by Django 3.1.3 on 2021-01-15 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itarmaterials', '0012_auto_20210114_2351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itarconstproperty',
            name='value',
            field=models.FloatField(null=True),
        ),
    ]