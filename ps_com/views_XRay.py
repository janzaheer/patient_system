from django.http import Http404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
from ps_com.forms import PatientXRayForm
from ps_com.models import PatientXRay
from django.views.generic import FormView, ListView, DeleteView
from ps_com.models import Patient
from django.views.generic import TemplateView


class PatientXRayView(FormView):
    form_class = PatientXRayForm
    template_name='XRay/create_XRay.html'

    # it will return user and its page

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse('login'))

        return super(PatientXRayView, self).dispatch(
            request, *args, **kwargs)

    # complete form should be valid then it will be submit

    def form_valid(self, form):
          obj = form.save(commit=False)
          obj.save()

          return HttpResponseRedirect(
                reverse('patient_xray',
                        kwargs={'patient_id': obj.patient.id}
                        )
           )

    # incase if data is invalid tha form will not be submit

    def form_invalid(self, form):
        return super(PatientXRayView, self).form_invalid(form)

    # this function get data and then sent data to fronthand

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

        # it will return user and its page

        def dispatch(self, request, *args, **kwargs):

            if not self.request.user.is_authenticated():
                return HttpResponseRedirect(reverse('login'))

            return super(
                PatientXrayListView, self).dispatch(
                request, *args, **kwargs)

        # this function create set

        def get_queryset(self):
            queryset = PatientXRay.objects.filter(
                patient=self.kwargs.get('patient_id')
            ).order_by('-id')
            return queryset

        # this function get data and then sent data to fronthand

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

class PatientXrayDeleteView(DeleteView):
            model = PatientXRay
            success_url = reverse_lazy('patient_list')
            success_message = "Delete Patient Xray Successfully"

            # it will return user and its page

            def dispatch(self, request, *args, **kwargs):
                if not self.request.user.is_authenticated():
                    return HttpResponseRedirect(reverse('login'))
                return super(
                    PatientXrayDeleteView, self).dispatch(
                    request, *args, **kwargs)

            def get(self, request, *args, **kwargs):
                    return self.post(request, *args, **kwargs)

