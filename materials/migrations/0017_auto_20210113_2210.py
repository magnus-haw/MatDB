# Generated by Django 3.1.3 on 2021-01-13 22:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0001_initial'),
        ('materials', '0016_auto_20210113_2202'),
    ]

    operations = [
        migrations.AddField(
            model_name='materialversion',
            name='material_expert',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='materials_materialversion_material_expert', to='contacts.person'),
        ),
        migrations.AddField(
            model_name='materialversion',
            name='material_lead',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='materials_materialversion_material_lead', to='contacts.person'),
        ),
        migrations.AddField(
            model_name='materialversion',
            name='modeling_expert',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='materials_materialversion_modeling_expert', to='contacts.person'),
        ),
        migrations.AddField(
            model_name='materialversion',
            name='other_contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='materials_materialversion_other_contact', to='contacts.person'),
        ),
    ]