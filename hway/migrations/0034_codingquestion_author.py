# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-07 13:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hway', '0033_codingquestion_solution_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='codingquestion',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hway.FacebookUser'),
        ),
    ]
