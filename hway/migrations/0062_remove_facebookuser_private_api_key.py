# Generated by Django 2.0.6 on 2018-06-27 18:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hway', '0061_auto_20180627_0508'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facebookuser',
            name='private_api_key',
        ),
    ]
