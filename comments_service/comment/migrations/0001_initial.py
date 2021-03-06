# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-08 08:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('entity', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='comment_text')),
                ('entity', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='entity.Entity', verbose_name='entity')),
                ('to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to', to='entity.Entity', verbose_name='comment_to')),
            ],
        ),
    ]
