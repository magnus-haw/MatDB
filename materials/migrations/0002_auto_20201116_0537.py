# Generated by Django 3.1.3 on 2020-11-16 05:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='constproperty',
            options={'verbose_name_plural': 'Constant properties'},
        ),
        migrations.AlterModelOptions(
            name='variableproperties',
            options={'verbose_name_plural': 'Variable properties'},
        ),
        migrations.AddField(
            model_name='constproperty',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='materialversion',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
