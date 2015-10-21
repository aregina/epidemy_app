# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('poster_url', models.URLField()),
                ('text', models.TextField()),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('city', models.CharField(default='', blank=True, max_length=100)),
                ('title', models.CharField(default='', blank=True, max_length=100)),
                ('place', models.CharField(default='', blank=True, max_length=100)),
            ],
        ),
    ]
