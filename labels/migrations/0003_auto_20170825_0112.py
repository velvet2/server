# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-25 01:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0002_remove_label_path'),
    ]

    operations = [
        migrations.RenameField(
            model_name='label',
            old_name='data',
            new_name='dat',
        ),
    ]
