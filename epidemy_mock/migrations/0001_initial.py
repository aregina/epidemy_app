# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='YupeConcerts',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('category_id', models.IntegerField(null=True, blank=True)),
                ('lang', models.CharField(null=True, max_length=2, blank=True)),
                ('creation_date', models.DateTimeField()),
                ('change_date', models.DateTimeField()),
                ('date', models.DateTimeField()),
                ('year', models.IntegerField()),
                ('title', models.CharField(max_length=150)),
                ('place', models.CharField(max_length=255)),
                ('alias', models.CharField(max_length=150)),
                ('short_text', models.TextField(null=True, blank=True)),
                ('full_text', models.TextField()),
                ('image', models.CharField(null=True, max_length=300, blank=True)),
                ('link', models.CharField(null=True, max_length=300, blank=True)),
                ('user_id', models.IntegerField()),
                ('status', models.IntegerField()),
                ('is_protected', models.IntegerField()),
                ('keywords', models.CharField(max_length=150)),
                ('description', models.CharField(max_length=250)),
            ],
            options={
                'managed': False,
                'db_table': 'yupe_concerts',
            },
        ),
        migrations.CreateModel(
            name='YupeNews',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('category_id', models.IntegerField(null=True, blank=True)),
                ('lang', models.CharField(null=True, max_length=2, blank=True)),
                ('creation_date', models.DateTimeField()),
                ('change_date', models.DateTimeField()),
                ('date', models.DateField()),
                ('title', models.CharField(max_length=150)),
                ('alias', models.CharField(max_length=150)),
                ('short_text', models.TextField(null=True, blank=True)),
                ('full_text', models.TextField()),
                ('image', models.CharField(null=True, max_length=300, blank=True)),
                ('link', models.CharField(null=True, max_length=300, blank=True)),
                ('user_id', models.IntegerField()),
                ('status', models.IntegerField()),
                ('is_protected', models.IntegerField()),
                ('keywords', models.CharField(max_length=150)),
                ('description', models.CharField(max_length=250)),
            ],
            options={
                'managed': False,
                'db_table': 'yupe_news',
            },
        ),
        migrations.CreateModel(
            name='Fan',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('fan_point', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('device_token', models.CharField(unique=True, max_length=255)),
                ('device_os_type', models.CharField(choices=[('I', 'ios'), ('A', 'android')], max_length=1)),
            ],
        ),
    ]
