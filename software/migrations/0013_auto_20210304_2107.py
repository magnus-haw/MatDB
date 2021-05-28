# Generated by Django 3.1.3 on 2021-03-04 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('software', '0012_auto_20210304_0107'),
    ]

    operations = [
        migrations.AddField(
            model_name='softwareversion',
            name='version_value',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='softwareversion',
            unique_together={('software', 'version')},
        ),
    ]