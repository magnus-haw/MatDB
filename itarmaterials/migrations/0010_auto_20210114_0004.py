# Generated by Django 3.1.3 on 2021-01-14 00:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0020_auto_20210114_0004'),
        ('itarmaterials', '0009_auto_20210113_2211'),
    ]

    operations = [
        migrations.AddField(
            model_name='itarconstproperty',
            name='material_version',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='materials.materialversion'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='itarmatrixproperty',
            name='material_version',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='materials.materialversion'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='itarreference',
            name='material_version',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='materials.materialversion'),
        ),
        migrations.AddField(
            model_name='itarvariableproperties',
            name='material_version',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='materials.materialversion'),
            preserve_default=False,
        ),
    ]
