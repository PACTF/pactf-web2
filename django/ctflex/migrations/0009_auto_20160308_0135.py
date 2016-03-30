# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-08 06:35
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ctflex', '0008_auto_20160228_2011'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=80)),
                ('body', models.TextField()),
                ('posted', models.DateTimeField(auto_now_add=True)),
                ('problems', models.ManyToManyField(to='ctflex.CtfProblem')),
            ],
        ),
        migrations.AlterField(
            model_name='window',
            name='codename',
            field=models.CharField(help_text='Human-readable identifier', max_length=30, unique=True, validators=[django.core.validators.RegexValidator(code='word_characters', message='Only alphanumeric characters and underscores are allowed.', regex='^\\w*$')]),
        ),
        migrations.AddField(
            model_name='competitor',
            name='unread_announcements',
            field=models.ManyToManyField(to='ctflex.Announcement'),
        ),
    ]
