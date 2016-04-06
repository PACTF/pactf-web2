# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-27 03:18
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields.jsonb
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField()),
                ('title', models.CharField(max_length=100)),
                ('title_html', models.CharField(blank=True, editable=False, max_length=100)),
                ('body', models.TextField()),
                ('body_html', models.TextField(blank=True, default='', editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Competitor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='CtfProblem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('points', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('description', models.TextField(blank=True, default='')),
                ('description_html', models.TextField(blank=True, default='', editable=False)),
                ('hint', models.TextField(blank=True, default='')),
                ('hint_html', models.TextField(blank=True, default='', editable=False)),
                ('grader', models.FilePathField(help_text="Basename of the problem's grading script in PROBLEMS_DIR", match='^.*\\.py$', max_length=200, path='/var/www/pactf/ctfproblems', recursive=True)),
                ('generator', models.FilePathField(blank=True, help_text="Basename of the problem's generator script in PROBLEMS_DIR", match='^.*\\.py$', max_length=200, null=True, path='/var/www/pactf/ctfproblems', recursive=True)),
                ('deps', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Problem',
            },
        ),
        migrations.CreateModel(
            name='Solve',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('flag', models.CharField(max_length=100)),
                ('competitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ctflex.Competitor')),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ctflex.CtfProblem')),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('p_id', models.UUIDField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('flag', models.CharField(blank=True, max_length=100)),
                ('correct', models.NullBooleanField()),
                ('competitor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ctflex.Competitor')),
                ('problem', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ctflex.CtfProblem')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='Team Name')),
                ('banned', models.BooleanField(default=False)),
                ('passphrase', models.CharField(max_length=30, verbose_name='Passphrase')),
                ('affiliation', models.CharField(blank=True, max_length=60, verbose_name='Affiliation')),
                ('country', models.CharField(choices=[('U', 'United States of America'), ('O', 'Other (ineligible for prizes)')], default='U', max_length=1)),
                ('background', models.CharField(choices=[('S', 'Middle-school/High-school'), ('O', 'Other (ineligible for prizes)')], default='S', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Timer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('start', models.DateTimeField(blank=True)),
                ('end', models.DateTimeField(blank=True)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ctflex.Team')),
            ],
        ),
        migrations.CreateModel(
            name='Window',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('codename', models.CharField(help_text='Human-readable identifier', max_length=30, unique=True, validators=[django.core.validators.RegexValidator(code='word_characters', message='Only alphanumeric characters and underscores are allowed.', regex='^\\w*$')])),
                ('verbose_name', models.CharField(help_text='User-facing title of window', max_length=30, unique=True)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('personal_timer_duration', models.DurationField()),
            ],
        ),
        migrations.AddField(
            model_name='timer',
            name='window',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ctflex.Window'),
        ),
        migrations.AddField(
            model_name='ctfproblem',
            name='window',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ctflex.Window'),
        ),
        migrations.AddField(
            model_name='competitor',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ctflex.Team'),
        ),
        migrations.AddField(
            model_name='competitor',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='announcement',
            name='competitors',
            field=models.ManyToManyField(blank=True, related_name='unread_announcements', to='ctflex.Competitor'),
        ),
        migrations.AddField(
            model_name='announcement',
            name='problems',
            field=models.ManyToManyField(blank=True, to='ctflex.CtfProblem'),
        ),
        migrations.AddField(
            model_name='announcement',
            name='window',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ctflex.Window'),
        ),
        migrations.AlterUniqueTogether(
            name='timer',
            unique_together=set([('window', 'team')]),
        ),
        migrations.AlterUniqueTogether(
            name='solve',
            unique_together=set([('problem', 'competitor')]),
        ),
    ]
