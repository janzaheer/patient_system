from django.http import Http404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from ps_com.forms import PatientXRayForm
from ps_com.models import PatientXRay
from django.views.generic import FormView, ListView
from ps_com.models import Patient
from django.views.generic import TemplateView


class PatientXRayView(FormView):
    form_class = PatientXRayForm
    template_name='XRay/create_XRay.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))

        return super(PatientXRayView, self).dispatch(
            request, *args, **kwargs)

    def form_valid(self, form):
          obj = form.save(commit=False)
          print self.request.POST.get('patient')
          print self.request.POST.get('added_date')
          print self.request.POST.get('image')
          print "_____________________"
          print "_____________________"
          print "_____________________"
          print "_____________________"
          print "_____________________"
          print "_____________________"
          obj.save()

          return HttpResponseRedirect(
                reverse('patient_xray',
                        kwargs={'patient_id': obj.patient.id}
                        )
           )

    def form_invalid(self, form):
        return super(PatientXRayView, self).form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super(
            PatientXRayView, self).get_context_data(**kwargs)
        context.update({
            'patient': Patient.objects.get(id=self.kwargs.get('pk'))
        })
        return context


class PatientXrayListView(ListView):
        model = PatientXRay
        paginate_by = 200
        template_name = 'XRay/patient_xray.html'

        def dispatch(self, request, *args, **kwargs):

            if not self.request.user.is_authenticated():
                return HttpResponseRedirect(reverse('login'))

            return super(
                PatientXrayListView, self).dispatch(
                request, *args, **kwargs)

        def get_queryset(self):
            queryset = PatientXRay.objects.filter(
                patient=self.kwargs.get('patient_id')
            ).order_by('-id')
            return queryset

        def get_context_data(self, **kwargs):
            context = super(
                PatientXrayListView, self).get_context_data(**kwargs)
            try:
                patient = Patient.objects.get(
                    id=self.kwargs.get('patient_id'))
            except:
                raise Http404('Patient Does not Exists!')

            context.update({
                'patient': patient
            })
            return context