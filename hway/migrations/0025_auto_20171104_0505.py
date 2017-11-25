# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-04 05:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hway', '0024_auto_20171104_0443'),
    ]

    operations = [
        migrations.RenameField(
            model_name='codingresult',
            old_name='current_score',
            new_name='possible_total',
        ),
        migrations.RemoveField(
            model_name='codingresult',
            name='previous_score',
        ),
        migrations.AddField(
            model_name='codingresult',
            name='scores',
            field=models.CharField(default='[]', max_length=1000000),
        ),
    ]
