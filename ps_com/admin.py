from __future__ import unicode_literals
from django.contrib import admin


from ps_com.models import Patient
from ps_com.models import AppointmentDetails
from ps_com.models import Billing, Clinic, ClinicUser, Doctor


class ClinicAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'phone', 'mobile', 'address', 'status'
    )


class ClinicUserAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'user'
    )

    @staticmethod
    def user(obj):
        return obj.user.username


class DoctorAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'doctor_id', 'clinic', 'designation', 'mobile', 'status'
    )


class PatientAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'patient_id', 'clinic', 'phone', 'sex', 'blood_group',
    )
    search_fields = ('patient_id', 'first_name', 'last_name', 'phone')


class AppointmentDetailsAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'appointment_id', 'doctor', 'clinic', 'appointment_date'
    )
    raw_id_fields = ('patient', 'doctor',)

    @staticmethod
    def patient_name(obj):
        return '%s %s' % (obj.patient.first_name, obj.patient.last_name)

    @staticmethod
    def patient_phone(obj):
        return '%s' % obj.patient.phone

    @staticmethod
    def doctor(obj):
        return obj.doctor.name


class BillingAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'doctor', 'appointment_id', 'clinic', 'discount',
        'amount', 'total', 'billing_date'
    )

    @staticmethod
    def appointment_id(obj):
        return obj.appointment.appointment_id

    @staticmethod
    def doctor(obj):
        return obj.apointment.doctor.name

    @staticmethod
    def total(obj):
        return obj.amount - obj.discount


admin.site.register(Patient, PatientAdmin)
admin.site.register(AppointmentDetails, AppointmentDetailsAdmin)
admin.site.register(Clinic, ClinicAdmin)
admin.site.register(ClinicUser, ClinicUserAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Billing, BillingAdmin)
