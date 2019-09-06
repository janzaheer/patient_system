from django import forms

from ps_com.models import Patient
from ps_com.models import AppointmentDetails
from ps_com.models import Billing, Doctor, PatientXRay

from django.http import Http404


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'


class AppointmentForm(forms.ModelForm):
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


class PatientXRayForm(forms.ModelForm):
    class Meta:
        model = PatientXRay
        fields = '__all__'