# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-29 14:57
from __future__ import unicode_literals

from django.db import migrations, models

from ctflex import models


def banned_to_standing(apps, schema_editor):
    Team = apps.get_model('ctflex', 'Team')
    for team in Team.objects.all():
        team.standing = models.Team.INVISIBLE_STANDING if team.banned else models.Team.GOOD_STANDING
        team.save()


def standing_to_banned(apps, schema_editor):
    Team = apps.get_model('ctflex', 'Team')
    for team in Team.objects.all():
        team.banned = team.standing != models.Team.GOOD_STANDING
        team.save()


class Migration(migrations.Migration):
    dependencies = [
        ('ctflex', '0014_team_standing'),
    ]

    operations = [
        migrations.RunPython(banned_to_standing, standing_to_banned),
    ]
