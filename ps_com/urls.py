"""patient_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from ps_com.views import (
    ReportsView, DashboardView, LoginView, LogoutView
)

from ps_com.views_billing import (
    CreateBillFormView, BillTemplateView, BillingList
)


from ps_com.view_doctor import (
    DoctorFormView, DoctorListView, DeletedoctorView,
    UpdatedoctorView, DoctorDetails, DoctorListView,
    DoctorAppoinmentsListView, UpdateAppointmentView,
    DoctorMonthlyReportsView
)


from ps_com.views_patient import (
    PatientAppoinmentsListView, PatientList, PatientDeleteView,
    PatientFormView, UpdatePatientView, PatientUpdateView,
    AddPatientAppointmentFormView, PatientAppointmentUpdateView
)

from ps_com.views_appointments import (
    UpdateAppointmentView, AppointmentListView, AppointmentForm,
    DeleteAppointmentView, AppointmentDetailsView
)

from ps_com.views_reports_api import (
    DailySalesAPI, MonthlySalesAPI
)

urlpatterns = [
    url(r'^$', DashboardView.as_view(), name='dashboard'),
    url(r'^reports/$', ReportsView.as_view(), name='reports'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),

    # Patient URLS
    url(r'^patient/list/$', PatientList.as_view(), name='patient_list'),
    url(r'^patient/add/$', PatientFormView.as_view(), name='patient_add'),
    url(
        r'^patient/(?P<pk>\d+)/delete/$',
        PatientDeleteView.as_view(),
        name='patient_delete'
    ),

    url(
        r'^patient/(?P<pk>\d+)/update/$',
        PatientUpdateView.as_view(),
        name='patient_update'
    ),

    url(
        r'^patient/(?P<patient_id>\d+)/appointment/add/$',
        AddPatientAppointmentFormView.as_view(),
        name='patient_add_appointment'
    ),

    url(
        r'^patient/(?P<patient_id>\d+)/appointments/$',
        PatientAppoinmentsListView.as_view(),
        name='patient_appointments'
    ),

    url(
        r'^patient/appointment/(?P<pk>\d+)/update/$',
        PatientAppointmentUpdateView.as_view(),
        name='patient_appointment_update'
    ),

    # Appointment URLS

    url(r'^appointment/list/$', AppointmentListView.as_view(),
        name='appointment_list'),



    url(
        r'^appointment/delete/(?P<pk>\d+)/$',
          DeleteAppointmentView.as_view(),
        name='appointment_delete'
    ),

    url(
        r'^appointment/(?P<pk>[a-zA-Z0-9_-]+)/details/$',
        AppointmentDetailsView.as_view(),
        name='appointment_details'
    ),
    url(
        r'^appointment/(?P<pk>\d+)/bill/create/$',
        CreateBillFormView.as_view(),
        name='create_appointment_bill'
    ),
    url(
        r'^appointment/(?P<pk>\d+)/update/$',
        UpdateAppointmentView.as_view(),
            name='update_appointment'
    ),

    # Bill URLS

    url(r'^billing-list/$', BillingList.as_view(), name='billing_list'),
    url(r'^create/bill/$', CreateBillFormView.as_view(), name='create_bill'),
    url(
        r'^bill/(?P<pk>\d+)/$',
        BillTemplateView.as_view(),
        name='bill_view'
    ),


    # Doctor Views
    url(
        r'^doctor/add/$', DoctorFormView.as_view(),
        name='doctor_add'
    ),
    url(
        r'^doctor/list/$', DoctorListView.as_view(),
        name='doctor_list'
    ),

    url(
        r'^doctor/(?P<pk>\d+)/update/$',
        UpdatedoctorView.as_view(),
        name='update'
    ),

    url(
        r'^doctor/delete/(?P<pk>\d+)/$',
        DeletedoctorView.as_view(),
        name='delete'
    ),

    url(
        r'^doctor/(?P<pk>[a-zA-Z0-9_-]+)/details/$',
        DoctorDetails.as_view(),
        name='details'
    ),

    url(
        r'^doctor/(?P<doctor_id>\d+)/appointments/$',
        DoctorAppoinmentsListView.as_view(),
        name='doctor_appointments'
    ),

    url(
        r'^doctor/appointment/(?P<pk>\d+)/update/$',
        UpdateAppointmentView.as_view(),
        name='update_doctor_appointment'
    ),
    url(
        r'^doctor/(?P<doctor_id>\d+)/monthly/reports/$',
        DoctorMonthlyReportsView.as_view(),
        name='doctor_monthly_reports'
    ),

    # Reports API URLS
    url(
        r'^daily/reports/$', DailySalesAPI.as_view(),
        name='daily_reports'
    ),
    url(
        r'^monthly/reports/$', MonthlySalesAPI.as_view(),
        name='monthly_reports'
    ),

]
