# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-03-08 11:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hway', '0059_auto_20180308_0915'),
    ]

    operations = [
        migrations.AddField(
            model_name='facebookuser',
            name='private_api_key',
            field=models.CharField(max_length=10000, null=True),
        ),
    ]
