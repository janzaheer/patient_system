# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse, reverse_lazy

from django.views.generic import (
    UpdateView, ListView, DeleteView, TemplateView
)
from django.http import HttpResponseRedirect


from ps_com.forms import AppointmentForm
from ps_com.models import Patient, Doctor
from ps_com.models import AppointmentDetails


class AppointmentListView(ListView):
    model = AppointmentDetails
    template_name = 'appointment/appointment_list.html'
    ordering = '-id'

    def dispatch(self, request, *args, **kwargs):

        if not self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))

        return super(
            AppointmentListView, self).dispatch(request, *args, **kwargs)


class DeleteAppointmentView(DeleteView):
    model = AppointmentDetails
    success_url = reverse_lazy('appointment_list')
    success_message = "Delete Appointment Successfully"

    def dispatch(self, request, *args, **kwargs):

        if not self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))

        return super(
            DeleteAppointmentView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class AppointmentDetailsView(TemplateView):
    template_name = 'appointment/appointment_details.html'

    def dispatch(self, request, *args, **kwargs):

        if not self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))

        return super(
            AppointmentDetailsView, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        try:
            return AppointmentDetails.objects.get(
                id=self.kwargs.get('pk'))
        except AppointmentDetails.DoesNotExist:
            raise Http404('Appointement Does not Exists!')

    def get_context_data(self, **kwargs):
        context = super(
            AppointmentDetailsView, self).get_context_data(**kwargs)
        context.update({
            'appointment': self.get_object()
        })
        return context


class UpdateAppointmentView(UpdateView):
    form_class = AppointmentForm
    template_name = 'appointment/appointment_update.html'
    model = AppointmentDetails
    success_url = reverse_lazy('appointment_list')

    def dispatch(self, request, *args, **kwargs):

        if not self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))

        return super(
            UpdateAppointmentView, self).dispatch(request, *args, **kwargs)


