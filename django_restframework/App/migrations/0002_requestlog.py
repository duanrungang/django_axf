# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-11-30 06:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('r_ip', models.CharField(max_length=32)),
                ('r_time', models.FloatField(default=0)),
            ],
        ),
    ]
