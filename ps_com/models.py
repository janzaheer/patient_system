import random
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils import timezone


class DatedModel(models.Model):
    class Meta:
        abstract = True

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Clinic(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField(
        max_length=500, blank=True, null=True
    )
    phone = models.CharField(
        max_length=20, blank=True, null=True
    )
    mobile = models.CharField(
        max_length=20, blank=True, null=True
    )
    status = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name.title()


class ClinicUser(models.Model):
    clinic = models.OneToOneField(Clinic, related_name='clinic_user')
    user = models.OneToOneField(User, related_name='user_clinic')

    def __unicode__(self):
        return self.clinic.name


class Doctor(models.Model):
    SEX_MALE = 'male'
    SEX_FEMALE = 'female'
    USER_SEX = (
        (SEX_MALE, 'Male'),
        (SEX_FEMALE, 'Female'),
    )

    BG_APLUS = 'A+'
    BG_AMINUS = 'A-'
    BG_BPLUS = 'B+'
    BG_BMINUS = 'B-'
    BG_OPLUS = '0+'
    BG_OMINUS = 'O-'
    BG_ABPLUS = 'AB+'
    BG_ABMINUS = 'AB-'

    BLOOD_GROUPS = (
        (BG_APLUS, 'A+'),
        (BG_AMINUS, 'A-'),
        (BG_BPLUS, 'B+'),
        (BG_BMINUS, 'B-'),
        (BG_OPLUS, 'O+'),
        (BG_OMINUS, 'O-'),
        (BG_ABPLUS, 'AB+'),
        (BG_ABMINUS, 'AB-'),

    )

    clinic = models.ForeignKey(
        Clinic, related_name='doctor_clinic', blank=True, null=True
    )
    doctor_id = models.CharField(max_length=7, blank=True, null=True)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200, blank=True, null=True)
    designation = models.CharField(max_length=200, blank=True, null=True)
    department = models.CharField(max_length=200, blank=True, null=True)
    address = models.TextField(
        max_length=500, blank=True, null=True
    )
    mobile = models.CharField(max_length=20)
    date_of_birth = models.DateField(blank=True, null=True)
    sex = models.CharField(
        max_length=10, choices=USER_SEX, blank=True, null=True
    )
    blood_group = models.CharField(
        max_length=10, choices=BLOOD_GROUPS, blank=True, null=True
    )
    status = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name.title()


class Patient(models.Model):
    SEX_MALE = 'male'
    SEX_FEMALE = 'female'
    USER_SEX = (
        (SEX_MALE, 'Male'),
        (SEX_FEMALE, 'Female'),
    )

    BG_APLUS = 'A+'
    BG_AMINUS = 'A-'
    BG_BPLUS = 'B+'
    BG_BMINUS = 'B-'
    BG_OPLUS = '0+'
    BG_OMINUS = 'O-'
    BG_ABPLUS = 'AB+'
    BG_ABMINUS = 'AB-'

    BLOOD_GROUPS = (
        (BG_APLUS, 'A+'),
        (BG_AMINUS, 'A-'),
        (BG_BPLUS, 'B+'),
        (BG_BMINUS, 'B-'),
        (BG_OPLUS, 'O+'),
        (BG_OMINUS, 'O-'),
        (BG_ABPLUS, 'AB+'),
        (BG_ABMINUS, 'AB-'),

    )
    clinic = models.ForeignKey(
        Clinic, related_name='patient_clinic', blank=True, null=True
    )
    patient_id = models.CharField(max_length=7, null=True, blank=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=13, blank=True, null=True)
    address = models.TextField(max_length=512, blank=True, null=True)

    cnic = models.CharField(max_length=20, blank=True, null=True)

    date_of_birth = models.DateField(blank=True, null=True)
    sex = models.CharField(
        max_length=10, choices=USER_SEX, blank=True, null=True
    )
    blood_group = models.CharField(
        max_length=10, choices=BLOOD_GROUPS, blank=True, null=True
    )

    def __unicode__(self):
        return '%s %s' % (self.first_name, self.last_name)


class AppointmentDetails(models.Model):

    STATUS_OPEN = "Open"
    STATUS_CANCELED = "Canceled"

    STATUSES = (
        (STATUS_OPEN, "Open"),
        (STATUS_CANCELED, "Canceled"),
    )

    clinic = models.ForeignKey(
        Clinic, related_name='appointment_clinic', blank=True, null=True
    )
    added_date = models.DateField(default=timezone.now, blank=True, null=True)
    appointment_id = models.CharField(max_length=7, blank=True, null=True)
    patient = models.ForeignKey(
        Patient, related_name='patient_details', blank=True, null=True
    )
    doctor = models.ForeignKey(
        Doctor, related_name='doctor_appointment', blank=True, null=True
    )
    procedure = models.TextField(max_length=500, blank=True, null=True)
    description = models.TextField(max_length=1000, blank=True, null=True)
    appointment_date = models.DateField(default=timezone.now, blank=True, null=True)
    appointment_time = models.CharField(
        max_length=200, blank=True, null=True,
        help_text="eg: AM 10:00"
    )
    clinical_notes = models.TextField(max_length=512, blank=True, null=True)
    status = models.CharField(
        choices=STATUSES, default=STATUS_OPEN, blank=True, null=True, max_length=200
    )

    def __unicode__(self):
        return '%s %s' % (
            self.patient.first_name, self.patient.last_name
        )  if self.patient else ''

    def has_bill(self):
        bill = self.appointment_bill.all()
        if bill.exists():
            return True
        else:
            return False

    def appointment_bill_id(self):
        latest_bill = self.appointment_bill.all().latest('id')
        return latest_bill.id

    def app_time(self):
        if self.appointment_time:
            app_time_list = self.appointment_time.split(' ')
            return app_time_list[1]

        return ''

    def app_time_format(self):
        if self.appointment_time:
            app_time_list = self.appointment_time.split(' ')
            return app_time_list[0]

        return ''


class Billing(models.Model):
    clinic = models.ForeignKey(
        Clinic, related_name='billing_clinic',
        blank=True, null=True
    )
    billing_date = models.DateField(
        default=timezone.now, blank=True, null=True
    )
    appointment = models.ForeignKey(
        AppointmentDetails, related_name="appointment_bill",
        blank=True, null=True
    )
    receipt_no = models.CharField(max_length=7, blank=True, null=True)
    amount = models.DecimalField(
        max_digits=8, decimal_places=2, default=0
    )
    discount = models.DecimalField(
        max_digits=8, decimal_places=2, default=0
    )

    def __unicode__(self):
        return self.receipt_no

    @property
    def paid_amount(self):
        return self.amount - self.discount


def create_save_patient_id(sender, instance, created, **kwargs):
    if not instance.patient_id:
        while True:
            random_code = random.randint(1000000, 9999999)
            if not Patient.objects.filter(patient_id=random_code).exists():
                break

        instance.patient_id = random_code
        instance.save()


def create_save_receipt_no(sender, instance, created, **kwargs):
    if not instance.receipt_no:
        while True:
            random_code = random.randint(1000000, 9999999)
            if not Patient.objects.filter(patient_id=random_code).exists():
                break

        instance.receipt_no = random_code
        instance.save()


def create_save_doctor_id(sender, instance, created, **kwargs):
    if not instance.doctor_id:
        while True:
            random_code = random.randint(1000000, 9999999)
            if not Patient.objects.filter(
                    patient_id=random_code).exists():
                break

        instance.doctor_id = random_code
        instance.save()


def create_save_appointment_id(sender, instance, created, **kwargs):
    if not instance.appointment_id:
        while True:
            random_code = random.randint(1000000, 9999999)
            if not AppointmentDetails.objects.filter(
                    appointment_id=random_code).exists():
                break

        instance.appointment_id = random_code
        instance.save()


# Signals
post_save.connect(create_save_patient_id, sender=Patient)
post_save.connect(create_save_receipt_no, sender=Billing)
post_save.connect(create_save_doctor_id, sender=Doctor)
post_save.connect(create_save_appointment_id, sender=AppointmentDetails)
