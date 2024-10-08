# Generated by Django 4.2.2 on 2024-08-24 16:10

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('lon', models.FloatField()),
                ('lat', models.FloatField()),
                ('owner', models.CharField(max_length=50)),
                ('ppoly', django.contrib.gis.db.models.fields.MultiPointField(srid=4326)),
            ],
        ),
    ]
