# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-04-02 07:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vblog', '0009_auto_20161101_1304'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='user',
        ),
    ]
