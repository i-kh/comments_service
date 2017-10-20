# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-19 14:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='commenthistory',
            name='type',
            field=models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], default='~', max_length=1),
            preserve_default=False,
        ),
    ]
