# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-24 15:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='label',
            name='path',
        ),
    ]
