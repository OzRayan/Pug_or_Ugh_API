# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2018-10-21 20:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pugorugh', '0003_auto_20181021_2127'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userdog',
            unique_together=set([]),
        ),
    ]
