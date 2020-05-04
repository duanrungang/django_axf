# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-10-24 01:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('FruitGP2', '0006_auto_20191023_2032'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('o_address', models.CharField(max_length=256)),
                ('o_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='FruitGP2.Order')),
            ],
        ),
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('a_address', models.CharField(max_length=256)),
                ('a_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FruitGP2.FruitUser')),
            ],
        ),
    ]
