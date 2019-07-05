# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DeleteView
from django.views.generic import FormView, ListView
from django.views.generic import TemplateView
from django.views.generic import UpdateView, RedirectView
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.http import Http404

from django.contrib.auth import forms as auth_forms
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from ps_com.forms import AppointmentForm, DoctorForm
from ps_com.forms import PatientForm
from ps_com.forms import BillingForm
from ps_com.models import Patient, Doctor
from ps_com.models import Billing, AppointmentDetails
from django.db import transaction


class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def dispatch(self, request, *args, **kwargs):

        if not self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))

        return super(DashboardView, self).dispatch(request, *args, **kwargs)


class IndexView(TemplateView):
    template_name = 'index.html'


class LoginView(FormView):
    template_name = 'login.html'
    form_class = auth_forms.AuthenticationForm
    success_url = reverse_lazy('dashboard')

    def dispatch(self, request, *args, **kwargs):

        if self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse('dashboard'))

        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        auth_login(self.request, user)
        return HttpResponseRedirect(reverse('dashboard'))

    def form_invalid(self, form):
        return super(LoginView, self).form_invalid(form)


class LogoutView(RedirectView):
    def dispatch(self, request, *args, **kwargs):
        auth_logout(self.request)
        return super(LogoutView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('login'))


class BillingList(TemplateView):
    template_name = 'bill/billing_list.html'

    def dispatch(self, request, *args, **kwargs):

        if not self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))

        return super(BillingList, self).dispatch(request, *args, **kwargs)

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

        if not self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))

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

    def dispatch(self, request, *args, **kwargs):

        if not self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))

        return super(
            BillTemplateView, self).dispatch(request, *args, **kwargs)

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
