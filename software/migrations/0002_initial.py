# Generated by Django 3.2.3 on 2021-06-08 19:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('software', '0001_initial'),
        ('sources', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('itarmaterials', '0002_initial'),
        ('materials', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='softwareversion',
            name='lead_developer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lead_developer', to='sources.person'),
        ),
        migrations.AddField(
            model_name='softwareversion',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='softwareversion',
            name='other_contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='other_contact', to='sources.person'),
        ),
        migrations.AddField(
            model_name='softwareversion',
            name='software',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='software.software'),
        ),
        migrations.AddField(
            model_name='software',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='software',
            name='point_of_contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='poc', to='sources.person'),
        ),
        migrations.AddField(
            model_name='itarexportformat',
            name='material_version',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='itarmaterials.itarmaterialversion'),
        ),
        migrations.AddField(
            model_name='itarexportformat',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='itarexportformat',
            name='software_version',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='software.softwareversion'),
        ),
        migrations.AddField(
            model_name='exportformat',
            name='material_version',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materials.materialversion'),
        ),
        migrations.AddField(
            model_name='exportformat',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='exportformat',
            name='software_version',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='software.softwareversion'),
        ),
        migrations.AlterUniqueTogether(
            name='softwareversion',
            unique_together={('software', 'version')},
        ),
    ]
