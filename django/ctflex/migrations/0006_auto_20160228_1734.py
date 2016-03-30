# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-28 22:34
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ctflex', '0005_auto_20160228_1730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='window',
            name='codename',
            field=models.CharField(help_text='Human-readable identifier', max_length=30, unique=True, validators=[django.core.validators.RegexValidator('^\\w*$', 'Only alphanumeric characters and underscores are allowed.')]),
        ),
    ]
