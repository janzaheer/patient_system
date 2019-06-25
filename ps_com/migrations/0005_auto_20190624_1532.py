# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-06-24 10:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ps_com', '0004_auto_20190624_1521'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointmentdetails',
            name='clinic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appointment_clinic', to='ps_com.Clinic'),
        ),
        migrations.AddField(
            model_name='billing',
            name='clinic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='billing_clinic', to='ps_com.Clinic'),
        ),
        migrations.AddField(
            model_name='doctor',
            name='clinic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doctor_clinic', to='ps_com.Clinic'),
        ),
        migrations.AddField(
            model_name='patient',
            name='clinic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='patient_clinic', to='ps_com.Clinic'),
        ),
    ]
