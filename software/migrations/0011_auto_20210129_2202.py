# Generated by Django 3.1.3 on 2021-01-29 22:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sources', '0001_initial'),
        ('software', '0010_delete_tutorial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='software',
            name='point_of_contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='poc', to='sources.person'),
        ),
        migrations.AlterField(
            model_name='softwareversion',
            name='lead_developer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lead_developer', to='sources.person'),
        ),
        migrations.AlterField(
            model_name='softwareversion',
            name='other_contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='other_contact', to='sources.person'),
        ),
    ]