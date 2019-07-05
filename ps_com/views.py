# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic import RedirectView, FormView, TemplateView
from django.http import HttpResponseRedirect
from django.utils import timezone

from django.contrib.auth import forms as auth_forms
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout

from ps_com.models import AppointmentDetails


class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def dispatch(self, request, *args, **kwargs):

        if not self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))

        return super(DashboardView, self).dispatch(request, *args, **kwargs)


class ReportsView(TemplateView):
    template_name = 'reports.html'

    def get_context_data(self, **kwargs):
        context = super(ReportsView, self).get_context_data(**kwargs)

        appointments = AppointmentDetails.objects.filter(
            appointment_date__icontains=timezone.now().date()
        )
        context.update({
            'appointments': appointments
        })
        return context


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

