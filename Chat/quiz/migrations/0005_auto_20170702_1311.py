# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-02 04:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_quiz_quiznum'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='answer_info',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
    ]