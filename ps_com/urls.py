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

from ps_com.views import IndexView
from ps_com.views import PatientList
from ps_com.views import PatientFormView
from ps_com.views import PatientDetails
from ps_com.views import PatientDeleteView
from ps_com.views import AddPatientDetailsFormView
from ps_com.views import BillingList
from ps_com.views import CreateBillFormView
from ps_com.views import PatientBillDisplayView
from ps_com.views import PatientEditView

urlpatterns = [
    url(r'^index/$', IndexView.as_view(), name='index'),
    url(r'^patient-list/$', PatientList.as_view(), name='patient_list'),
    url(r'^patient-add/$', PatientFormView.as_view(), name='patient_add'),
    url(
        r'^patient-delete/(?P<pk>\d+)/$',
        PatientDeleteView.as_view(),
        name='patient_delete'
    ),
    url(
        r'^patient/(?P<patient_id>[a-zA-Z0-9_-]+)/details/$',
        PatientDetails.as_view(),
        name='patient_details'
    ),
    url(
        r'^patient/(?P<patient_id>[a-zA-Z0-9_-]+)/details/add/$',
        AddPatientDetailsFormView.as_view(),
        name='add_patient_details'
    ),

    url(r'^billing-list/$', BillingList.as_view(), name='billing_list'),
    url(r'^create/bill/$', CreateBillFormView.as_view(), name='create_bill'),
    url(
        r'^patient/bill/(?P<pk>\d+)/$',
        PatientBillDisplayView.as_view(),
        name='patient_bill'
    ),
    url(
        r'^patient/(?P<pk>\d+)/edit_patient/$',
        PatientEditView.as_view(),
        name='edit_patient'
    ),

]
