# Generated by Django 3.1.3 on 2021-01-13 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0014_auto_20210113_0718'),
    ]

    operations = [
        migrations.AddField(
            model_name='reference',
            name='link',
            field=models.URLField(blank=True, null=True),
        ),
    ]