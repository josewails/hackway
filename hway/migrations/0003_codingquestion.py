# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-17 15:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hway', '0002_auto_20171014_1104'),
    ]

    operations = [
        migrations.CreateModel(
            name='CodingQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('question', models.TextField()),
                ('sample_input', models.CharField(max_length=1000000)),
                ('sample_output', models.CharField(max_length=1000000)),
                ('input', models.CharField(max_length=10000000)),
                ('output', models.CharField(max_length=10000000)),
            ],
        ),
    ]
