# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-23 15:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hway', '0054_auto_20171123_1348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programmingquestion',
            name='course_segment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='programming_questions', to='hway.CourseSegment'),
        ),
    ]