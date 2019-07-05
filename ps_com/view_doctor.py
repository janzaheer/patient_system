from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.http import Http404

from ps_com.forms import DoctorForm, AppointmentForm
from django.views.generic import DeleteView
from django.views.generic import FormView, ListView
from django.views.generic import TemplateView
from django.views.generic import UpdateView
from ps_com.models import Doctor, AppointmentDetails, Patient


class DoctorFormView(FormView):
    form_class = DoctorForm
    template_name = 'doctor/add.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))

        return super(
            DoctorFormView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('doctor_list'))

    def form_invalid(self, form):
        return super(DoctorFormView, self).form_invalid(form)


class DoctorListView(ListView):
    model = Doctor
    paginate_by = 100
    template_name = 'doctor/list.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))

        return super(
            DoctorListView, self).dispatch(request, *args, **kwargs)


class UpdatedoctorView(UpdateView):
    form_class = DoctorForm
    template_name = 'doctor/update.html'
    model = Doctor

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))

        return super(
            UpdatedoctorView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        return HttpResponseRedirect(reverse('doctor_list'))


class DeletedoctorView(DeleteView):
    model = Doctor
    success_url = reverse_lazy('doctor_list')
    success_message = "Delete Doctor Successfully"

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))

        return super(
            DeletedoctorView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class DoctorDetails(TemplateView):
    template_name = 'doctor/details.html'

    def dispatch(self, request, *args, **kwargs):

        if not self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))

        return super(
            DoctorDetails, self).dispatch(request, *args, **kwargs)

    def get_object(self):
        try:
            return Doctor.objects.get(
                id=self.kwargs.get('pk'))
        except Doctor.DoesNotExist:
            raise Http404('Doctor Does not Exists!')

    def get_context_data(self, **kwargs):
        context = super(DoctorDetails, self).get_context_data(**kwargs)
        doctor = self.get_object()
        context.update({
            'doctor': self.get_object()
        })
        return context


class DoctorAppoinmentsListView(ListView):
    model = AppointmentDetails
    paginate_by = 200
    template_name = 'doctor/doctor_appointment_list.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))

        return super(
            DoctorAppoinmentsListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = AppointmentDetails.objects.filter(
            doctor=self.kwargs.get('doctor_id')
        ).order_by('appointment_date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(
            DoctorAppoinmentsListView, self).get_context_data(**kwargs)
        try:
            doctor = Doctor.objects.get(
                id=self.kwargs.get('doctor_id'))
        except:
            raise Http404('Doctor Does not Exists!')

        context.update({
            'doctor': doctor
        })
        return context


class UpdateAppointmentView(UpdateView):
    form_class = AppointmentForm
    template_name = 'doctor/update_appointment.html'
    model = AppointmentDetails

    def dispatch(self, request, *args, **kwargs):

        if not self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))

        return super(
            UpdateAppointmentView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save()
        return HttpResponseRedirect(
            reverse('doctor_appointments',
                    kwargs={'doctor_id': obj.doctor.id})
        )
