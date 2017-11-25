# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-09 11:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hway', '0035_auto_20171108_1041'),
    ]

    operations = [
        migrations.AddField(
            model_name='programminglanguage',
            name='logo',
            field=models.ImageField(null=True, upload_to='programming_languages_logos'),
        ),
        migrations.AddField(
            model_name='programmingquestion',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hway.FacebookUser'),
        ),
    ]
