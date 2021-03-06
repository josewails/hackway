# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-09 17:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hway', '0037_auto_20171109_1224'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='programmingcategory',
            options={'verbose_name_plural': 'Programming Categories'},
        ),
        migrations.AddField(
            model_name='botuser',
            name='challenge_data',
            field=models.CharField(max_length=100000, null=True),
        ),
        migrations.AddField(
            model_name='botuser',
            name='challenged',
            field=models.BooleanField(default=False),
        ),
    ]
