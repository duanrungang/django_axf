# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-11-30 03:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('b_title', models.CharField(max_length=32)),
                ('b_content', models.TextField()),
            ],
        ),
    ]
