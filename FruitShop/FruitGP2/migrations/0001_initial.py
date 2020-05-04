# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-10-21 13:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FruitUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('f_name', models.CharField(max_length=32, unique=True)),
                ('f_password', models.CharField(max_length=256)),
                ('f_age', models.IntegerField(default=1)),
                ('f_sex', models.BooleanField(default=False)),
                ('is_delete', models.BooleanField(default=False)),
                ('is_forbidden', models.BooleanField(default=False)),
                ('f_email', models.CharField(max_length=64, unique=True)),
                ('f_register_date', models.DateTimeField(auto_now_add=True)),
                ('f_icon', models.CharField(max_length=128, null=True)),
                ('is_active', models.BooleanField(default=False)),
            ],
        ),
    ]
