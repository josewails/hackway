# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-03-08 09:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hway', '0058_auto_20171124_0355'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facebookuser',
            name='private_api_key',
        ),
        migrations.RemoveField(
            model_name='facebookuser',
            name='public_api_key',
        ),
    ]
