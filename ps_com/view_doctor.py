from __future__ import unicode_literals

import datetime
from calendar import monthrange

from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.http import Http404
from django.utils import timezone
from django.db.models import Sum
from dateutil.relativedelta import relativedelta

from ps_com.forms import DoctorForm, AppointmentForm
from django.views.generic import DeleteView
from django.views.generic import FormView, ListView
from django.views.generic import TemplateView
from django.views.generic import UpdateView
from ps_com.models import Doctor, AppointmentDetails, Billing


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

    def get_queryset(self):
        queryset= self.queryset
        if not queryset:
            queryset = Doctor.objects.filter(
                clinic=self.request.user.user_clinic.clinic)

            return queryset.order_by('-id')


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


class DoctorMonthlyReportsView(TemplateView):
    template_name = 'doctor/monthly_reports.html'

    @staticmethod
    def sales_data(obj, month_date=None):
        bill_amount = obj.aggregate(
            total_bill=Sum('amount')
        )
        total_bill = (
            int(bill_amount.get('total_bill')) if
            bill_amount.get('total_bill') else 0
        )
        bill_discount = obj.aggregate(
            total_discount=Sum('discount')
        )

        total_discount = (
            int(bill_discount.get('total_discount')) if
            bill_discount.get('total_discount') else 0
        )

        total = total_bill - total_discount

        data = {
            'amount': total_bill,
            'discount': total_discount,
            'total': total,
        }

        data.update({
            'day': month_date.strftime('%B')
        })

        return data

    def get_context_data(self, **kwargs):
        context = super(
            DoctorMonthlyReportsView, self).get_context_data(**kwargs)

        date_month = timezone.now()
        month_range = monthrange(
            date_month.year, date_month.month
        )
        start_month = datetime.datetime(
            date_month.year, date_month.month, 1)

        end_month = datetime.datetime(
            date_month.year, date_month.month, month_range[1]
        )
        monthly_bills = Billing.objects.filter(
            appointment__doctor__id=self.kwargs.get('doctor_id'),
            billing_date__gte=start_month,
            billing_date__lt=end_month.replace(
                        hour=23, minute=59, second=59)
        )

        reports = []
        for month in range(12):
            date_month = timezone.now() - relativedelta(months=month)
            month_range = monthrange(
                date_month.year, date_month.month
            )
            start_month = datetime.datetime(
                date_month.year, date_month.month, 1)

            end_month = datetime.datetime(
                date_month.year, date_month.month, month_range[1]
            )

            billing = Billing.objects.filter(
                appointment__doctor__id=self.kwargs.get('doctor_id'),
                billing_date__gte=start_month,
                billing_date__lt=end_month.replace(
                        hour=23, minute=59, second=59)
            )

            data = self.sales_data(
                obj=billing, month_date=end_month
            )

            reports.append(data)

        context.update({
            'monthly_bills': monthly_bills,
            'monthly_reports': reports,
            'doctor': Doctor.objects.get(id=self.kwargs.get('doctor_id'))
        })

        return context
