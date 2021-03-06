# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-24 14:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0002_project_label'),
        ('datas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('config', models.TextField()),
                ('path', models.TextField()),
                ('data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='datas', to='datas.Data')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='projects.Project')),
            ],
            options={
                'ordering': ('created',),
            },
        ),
    ]
