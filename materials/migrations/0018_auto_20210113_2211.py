# Generated by Django 3.1.3 on 2021-01-13 22:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0001_initial'),
        ('materials', '0017_auto_20210113_2210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materialversion',
            name='material_expert',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='materialversion_material_expert', to='contacts.person'),
        ),
        migrations.AlterField(
            model_name='materialversion',
            name='material_lead',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='materialversion_material_lead', to='contacts.person'),
        ),
        migrations.AlterField(
            model_name='materialversion',
            name='modeling_expert',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='materialversion_modeling_expert', to='contacts.person'),
        ),
        migrations.AlterField(
            model_name='materialversion',
            name='other_contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='materialversion_other_contact', to='contacts.person'),
        ),
    ]
