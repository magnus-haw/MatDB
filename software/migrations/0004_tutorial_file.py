# Generated by Django 3.1.3 on 2021-01-23 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('software', '0003_softwareversion_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutorial',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
