# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-24 14:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='label',
            field=models.CharField(choices=[('class', 'Classification'), ('bbox', 'Bounding Box'), ('locate', 'Locating')], default='class', max_length=10),
        ),
    ]