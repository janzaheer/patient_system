# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-06-24 10:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ps_com', '0003_auto_20190624_1416'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointmentdetails',
            old_name='doctor_name',
            new_name='doctor',
        ),
    ]
