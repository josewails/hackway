# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-23 21:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hway', '0056_botuser_solving_course_quiz'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='current_segment_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
