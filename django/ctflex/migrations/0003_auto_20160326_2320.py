# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-27 03:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ctflex', '0002_auto_20160326_2318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='affiliation',
            field=models.CharField(blank=True, max_length=60, verbose_name='School'),
        ),
    ]
