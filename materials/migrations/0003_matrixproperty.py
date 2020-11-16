# Generated by Django 3.1.3 on 2020-11-16 06:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0002_auto_20201116_0537'),
    ]

    operations = [
        migrations.CreateModel(
            name='MatrixProperty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
                ('value', models.CharField(max_length=500)),
                ('state', models.PositiveIntegerField(choices=[(0, 'Virgin'), (1, 'Char'), (2, 'Pyrolysis')], default=0)),
                ('last_modified', models.DateField(auto_now=True)),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materials.materialversion')),
            ],
            options={
                'verbose_name_plural': 'Matrix properties',
            },
        ),
    ]
