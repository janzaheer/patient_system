from __future__ import unicode_literals
from django.contrib import admin


from ps_com.models import Patient
from ps_com.models import AppointmentDetails
from ps_com.models import Billing


class PatientAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'patient_id', 'phone', 'sex',
        'blood_group', 'created_at'
    )
    search_fields = ('patient_id', 'first_name', 'last_name', 'phone')


class AppointmentDetailsAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'patient_name', 'patient_phone',
        'doctor_name', 'detail', 'created_at'
    )
    search_fields = (
        'patient__patient_id', 'patient__first_name', 'patient__last_name',
        'patient__phone', 'doctor_name'
    )
    raw_id_fields = ('patient',)

    @staticmethod
    def patient_name(obj):
        return '%s %s' % (obj.patient.first_name, obj.patient.last_name)

    @staticmethod
    def patient_phone(obj):
        return '%s' % obj.patient.phone


class BillingAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'patient_name', 'patient_phone', 'discount',
        'amount', 'total', 'created_at'
    )
    search_fields = (
        'patient__patient_id', 'patient__first_name', 'patient__last_name',
        'patient__phone', 'doctor_name'
    )
    raw_id_fields = ('patient',)

    @staticmethod
    def patient_name(obj):
        return '%s %s' % (obj.patient.first_name, obj.patient.last_name)

    @staticmethod
    def patient_phone(obj):
        return '%s' % obj.patient.phone

    @staticmethod
    def total(obj):
        return obj.amount - obj.discount


admin.site.register(Patient, PatientAdmin)
admin.site.register(AppointmentDetails, AppointmentDetailsAdmin)
admin.site.register(Billing, BillingAdmin)
