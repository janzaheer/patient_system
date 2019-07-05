from django.views.generic import (
    FormView, ListView, TemplateView, DeleteView,
    UpdateView
)
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction

from ps_com.models import AppointmentDetails, Patient, Doctor
from ps_com.forms import PatientForm, AppointmentForm


class PatientList(TemplateView):
    template_name = 'patient/patient_list.html'

    @staticmethod
    def get_patients():
        """
        returns all patients
        :return:
        """
        return Patient.objects.all().order_by('id')

    def get_context_data(self, **kwargs):
        context = super(PatientList, self).get_context_data(**kwargs)

        context.update({
            'patients': self.get_patients()
        })
        return context


class PatientFormView(FormView):
    template_name = 'patient/patient_add.html'
    form_class = PatientForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(PatientFormView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        patient = form.save()
        return HttpResponseRedirect(reverse('patient_list'))

    def form_invalid(self, form):
        print form.errors
        print 'coming here -------------------------'
        return HttpResponseRedirect(reverse('patient_list'))

class UpdatePatientView(UpdateView):
    form_class = PatientForm
    template_name = 'patient/patient_update.html'
    model = Patient

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.save()
        return HttpResponseRedirect(reverse('patient_list'))

class PatientUpdateView(UpdateView):
    form_class = PatientForm
    template_name = 'patient/patient_update.html'
    model = Patient
    success_url = reverse_lazy('patient_list')


class PatientDeleteView(DeleteView):
    model = Patient
    success_url = reverse_lazy('patient_list')
    success_message = "Delete Patient Successfully"

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class AddPatientAppointmentFormView(FormView):
    template_name = 'patient/add_patient_appointment.html'
    form_class = AppointmentForm

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(
            AddPatientAppointmentFormView, self).dispatch(
            request, *args, **kwargs)

    def form_valid(self, form):
        with transaction.atomic():
            obj = form.save(commit=False)
            obj.doctor = Doctor.objects.get(
                name=self.request.POST.get('doctor_name')
            )
            obj.save()
            return HttpResponseRedirect(reverse('patient_list'))

    def form_invalid(self, form):
        return super(AddPatientAppointmentFormView, self).form_invalid(form)

    def get_patient_object(self):
        try:
            return Patient.objects.get(
                id=self.kwargs.get('patient_id'))
        except Patient.DoesNotExist:
            raise Http404('Patient Does not Exists!')

    def get_context_data(self, **kwargs):
        context = super(
            AddPatientAppointmentFormView, self).get_context_data(**kwargs)

        context.update({
            'patient': self.get_patient_object(),
            'doctors': Doctor.objects.all().order_by('name')
        })
        return context


class PatientAppoinmentsListView(ListView):
    model = AppointmentDetails
    paginate_by = 200
    template_name = 'patient/patient_appointment_list.html'

    def get_queryset(self):
        queryset = AppointmentDetails.objects.filter(
            patient=self.kwargs.get('patient_id')
        ).order_by('appointment_date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(
            PatientAppoinmentsListView, self).get_context_data(**kwargs)
        try:
            patient = Patient.objects.get(
                id=self.kwargs.get('patient_id'))
        except:
            raise Http404('Patient Does not Exists!')

        context.update({
            'patient': patient
        })
        return context


class PatientAppointmentUpdateView(UpdateView):
    form_class = AppointmentForm
    template_name = 'patient/patient_appointment_update.html'
    model = AppointmentDetails


    def form_valid(self, form):
        obj = form.save()

        return HttpResponseRedirect(
            reverse('patient_appointment_list',
                    kwargs={'patient_id': obj.patient.id}
                    )
        )