# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-05-06 16:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('osis_common', '0017_auto_20190506_1609'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messagehistory',
            name='receiver_person_id',
            field=models.IntegerField(blank=True, db_index=True, null=True),
        ),
    ]
