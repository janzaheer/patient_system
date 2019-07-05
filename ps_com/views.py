# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DeleteView
from django.views.generic import FormView, ListView
from django.views.generic import TemplateView
from django.views.generic import UpdateView
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.http import Http404

from ps_com.forms import AppointmentForm, DoctorForm
from ps_com.forms import PatientForm
from ps_com.forms import BillingForm
from ps_com.models import Patient, Doctor
from ps_com.models import Billing, AppointmentDetails
from django.db import transaction

class DashboardView(TemplateView):
    template_name = 'dashboard.html'


class IndexView(TemplateView):
    template_name = 'index.html'


class AppointmentListView(ListView):
    model = AppointmentDetails
    template_name = 'appointment/appointment_list.html'
    ordering = '-id'


class DeleteAppointmentView(DeleteView):
    model = AppointmentDetails
    success_url = reverse_lazy('appointment_list')
    success_message = "Delete Appointment Successfully"

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class AppointmentDetailsView(TemplateView):
    template_name = 'appointment/appointment_details.html'

    def get_object(self):
        try:
            return AppointmentDetails.objects.get(
                id=self.kwargs.get('pk'))
        except AppointmentDetails.DoesNotExist:
            raise Http404('Appointement Does not Exists!')

    def get_context_data(self, **kwargs):
        context = super(AppointmentDetailsView, self).get_context_data(**kwargs)
        appointment = self.get_object()
        context.update({
            'appointment': self.get_object()
        })
        return context


class BillingList(TemplateView):
    template_name = 'bill/billing_list.html'

    @staticmethod
    def get_bills():
        return Billing.objects.all().order_by('id')

    def get_context_data(self, **kwargs):
        context = super(BillingList, self).get_context_data(**kwargs)
        context.update({
            'bills': self.get_bills()
        })
        return context


class CreateBillFormView(FormView):
    form_class = BillingForm
    template_name = 'bill/create_bill.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(
            CreateBillFormView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save()
        return HttpResponseRedirect(reverse('bill_view', kwargs={'pk': obj.id}))

    def form_invalid(self, form):
        return super(CreateBillFormView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateBillFormView, self).get_context_data(**kwargs)
        try:
            appointment = AppointmentDetails.objects.get(id=self.kwargs.get('pk'))
        except:
            raise Http404('Appointment does not exists!')
        context.update({
            'appointment': appointment
        })
        return context


class BillTemplateView(TemplateView):
    template_name = 'bill/bill_display.html'

    def get_bill_object(self):
        try:
            return Billing.objects.get(pk=self.kwargs.get('pk'))
        except Billing.DoesNotExist:
            raise Http404('Bill not found')

    def get_context_data(self, **kwargs):
        context = super(
            BillTemplateView, self).get_context_data(**kwargs)

        context.update({
            'bill': self.get_bill_object()
        })
        return context

#
# class DoctorFormView(FormView):
#     form_class = DoctorForm
#     template_name = 'doctor/add.html'
#
#
#     def form_valid(self, form):
#         form.save()
#         return HttpResponseRedirect(reverse('doctor_list'))
#
#     def form_invalid(self, form):
#         return super(DoctorFormView, self).form_invalid(form)
#
#
# class DoctorListView(ListView):
#     model = Doctor
#     paginate_by = 100
#     template_name = 'doctor/list.html'
#
#
# class UpdatedoctorView(UpdateView):
#     form_class = DoctorForm
#     template_name = 'doctor/update.html'
#     model = Doctor
#
#     def form_valid(self, form):
#         obj = form.save(commit=False)
#         obj.save()
#         return HttpResponseRedirect(reverse('doctor_list'))
#
# class DeletedoctorView(DeleteView):
#     model = Doctor
#     success_url = reverse_lazy('doctor_list')
#     success_message = "Delete Doctor Successfully"
#
#     def get(self, request, *args, **kwargs):
#         return self.post(request, *args, **kwargs)
#
# class DoctorDetails(TemplateView):
#     template_name = 'doctor/details.html'
#
#     def get_object(self):
#         try:
#             return Doctor.objects.get(
#                 id=self.kwargs.get('pk'))
#         except Doctor.DoesNotExist:
#             raise Http404('Doctor Does not Exists!')
#
#     def get_context_data(self, **kwargs):
#         context = super(DoctorDetails, self).get_context_data(**kwargs)
#         doctor = self.get_object()
#         context.update({
#             'doctor': self.get_object()
#         })
#         return context
