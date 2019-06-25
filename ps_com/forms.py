from django import forms

from ps_com.models import Patient
from ps_com.models import AppointmentDetails
from ps_com.models import Billing, Doctor

from django.http import Http404


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'first_name', 'last_name', 'phone', 'address',
            'date_of_birth','sex', 'blood_group'
        ]


class PatientDetailForm(forms.ModelForm):
    class Meta:
        model = AppointmentDetails
        fields = '__all__'


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = '__all__'


class BillingForm(forms.ModelForm):
    class Meta:
        model = Billing
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        patient_id = kwargs.pop('patient', None)
        super(BillingForm, self).__init__(*args, **kwargs)
        if patient_id:
            try:
                self.patient = Patient.objects.get(pk=patient_id)
            except Patient.DoesNotExist:
                raise Http404('Patient %s does not exists')

    def save(self, commit=True):
        instance = super(BillingForm, self).save(commit=False)
        instance.patient = self.patient
        instance.save()
        return instance
