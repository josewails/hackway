# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-21 20:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hway', '0050_coursesegment_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='programmingcategory',
            name='published',
            field=models.BooleanField(default=False),
        ),
    ]