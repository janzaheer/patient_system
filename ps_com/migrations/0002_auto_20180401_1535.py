# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-01 10:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ps_com', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billing',
            name='patient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='patient_billing', to='ps_com.Patient'),
        ),
    ]
