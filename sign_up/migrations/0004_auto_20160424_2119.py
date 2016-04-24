# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-24 21:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sign_up', '0003_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='signup',
            name='address',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='signup',
            name='birth_year',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
