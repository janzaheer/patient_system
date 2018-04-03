# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DeleteView
from django.views.generic import FormView
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.http import Http404

from ps_com.forms import PatientDetailForm
from ps_com.forms import PatientForm
from ps_com.forms import BillingForm
from ps_com.models import Patient
from ps_com.models import Billing


class IndexView(TemplateView):
    template_name = 'index.html'


class PatientList(TemplateView):
    template_name = 'patient_list.html'

    @staticmethod
    def get_patients():
        """
        returns all patients
        :return:
        """
        return Patient.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super(PatientList, self).get_context_data(**kwargs)

        context.update({
            'patients': self.get_patients()
        })
        return context


class PatientFormView(FormView):
    template_name = 'patient_add.html'
    form_class = PatientForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PatientFormView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        patient = form.save()
        return HttpResponseRedirect(reverse('patient_list'))

    def form_invalid(self, form):
        return HttpResponseRedirect(reverse('patient_list'))


class PatientDeleteView(DeleteView):
    model = Patient
    success_url = reverse_lazy('patient_list')
    success_message = "Delete Patient Successfully"

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class PatientDetails(TemplateView):
    template_name = 'patient_details.html'

    def get_object(self):
        try:
            return Patient.objects.get(
                patient_id=self.kwargs.get('patient_id'))
        except Patient.DoesNotExist:
            raise Http404('Patient Does not Exists!')

    def get_context_data(self, **kwargs):
        context = super(PatientDetails, self).get_context_data(**kwargs)
        patient = self.get_object()
        context.update({
            'patient_details': (
                patient.patient_details.all().order_by('-created_at')),
            'patient': self.get_object()
        })
        return context


class AddPatientDetailsFormView(FormView):
    template_name = 'add_patient_details.html'
    form_class = PatientDetailForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(
            AddPatientDetailsFormView, self).dispatch(
            request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('patient_list'))
    
    def form_invalid(self, form):
        return super(AddPatientDetailsFormView, self).form_invalid(form)

    def get_patient_object(self):
        try:
            return Patient.objects.get(
                patient_id=self.kwargs.get('patient_id'))
        except Patient.DoesNotExist:
            raise Http404('Patient Does not Exists!')

    def get_context_data(self, **kwargs):
        context = super(
            AddPatientDetailsFormView, self).get_context_data(**kwargs)

        context.update({
            'patient': self.get_patient_object()
        })
        return context


class BillingList(TemplateView):
    template_name = 'billing_list.html'

    @staticmethod
    def get_bills():
        return Billing.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super(BillingList, self).get_context_data(**kwargs)
        context.update({
            'bills': self.get_bills()
        })
        return context


class CreateBillFormView(FormView):
    form_class = BillingForm
    template_name = 'create_bill.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(
            CreateBillFormView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateBillFormView, self).get_form_kwargs()
        if self.request.method in ('POST', 'PUT'):
            try:
                patient = Patient.objects.get(
                    patient_id=self.request.POST.get('patient_id')
                )
            except Patient.DoesNotExist:
                raise Http404(
                    'Patient %s does not '
                    'exist' % self.request.POST.get('patient_id')
                )
            kwargs.update({
                'patient': patient.id
            })
        return kwargs

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('billing_list'))

    def form_invalid(self, form):
        return super(CreateBillFormView, self).form_invalid(form)


class PatientBillDisplayView(TemplateView):
    template_name = 'bill_display.html'

    def get_bill_object(self):
        try:
            return Billing.objects.get(pk=self.kwargs.get('pk'))
        except Billing.DoesNotExist:
            raise Http404('Bill not found')

    def get_context_data(self, **kwargs):
        context = super(
            PatientBillDisplayView, self).get_context_data(**kwargs)

        context.update({
            'bill': self.get_bill_object()
        })
        return context
