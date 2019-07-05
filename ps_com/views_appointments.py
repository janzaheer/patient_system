# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse, reverse_lazy

from django.views.generic import UpdateView
from django.http import HttpResponseRedirect


from ps_com.forms import AppointmentForm
from ps_com.models import Patient, Doctor
from ps_com.models import AppointmentDetails

class UpdateAppointmentView(UpdateView):
    form_class = AppointmentForm
    template_name = 'appointment/appointment_update.html'
    model = AppointmentDetails
    success_url = reverse_lazy('appointment_list')


