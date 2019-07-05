# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView, TemplateView
from django.http import HttpResponseRedirect, Http404

from ps_com.forms import BillingForm
from ps_com.models import Billing, AppointmentDetails


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