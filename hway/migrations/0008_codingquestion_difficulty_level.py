# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-26 13:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hway', '0007_auto_20171021_1003'),
    ]

    operations = [
        migrations.AddField(
            model_name='codingquestion',
            name='difficulty_level',
            field=models.CharField(choices=[('1', 'simple'), ('2', 'medium'), ('3', 'difficult')], max_length=10, null=True),
        ),
    ]
