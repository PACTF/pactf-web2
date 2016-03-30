# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-23 07:06
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ctflex', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('a_id', models.IntegerField()),
                ('title', models.CharField(max_length=80)),
                ('body', models.TextField()),
                ('posted', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='team',
            name='password',
        ),
        migrations.AddField(
            model_name='team',
            name='passphrase',
            field=models.CharField(default='test', max_length=30, verbose_name='Passphrase'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ctfproblem',
            name='deps',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='ctfproblem',
            name='points',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='team',
            name='affiliation',
            field=models.CharField(blank=True, max_length=60, verbose_name='Affiliation'),
        ),
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(max_length=30, unique=True, verbose_name='Team Name'),
        ),
        migrations.AddField(
            model_name='announcement',
            name='problems',
            field=models.ManyToManyField(to='ctflex.CtfProblem'),
        ),
        migrations.AddField(
            model_name='competitor',
            name='unread_announcements',
            field=models.ManyToManyField(to='ctflex.Announcement'),
        ),
    ]
