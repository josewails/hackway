# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-11 11:42
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hway', '0039_auto_20171111_1141'),
    ]

    operations = [
        migrations.RenameField(
            model_name='botuser',
            old_name='challenge_data',
            new_name='quiz_data',
        ),
    ]
