# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-21 17:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wikiapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wikipathstep',
            name='game',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wikiapp.WikiGame'),
        ),
    ]
