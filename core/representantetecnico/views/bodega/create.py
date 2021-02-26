from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins import ValidatePermissionRequiredMixin
from core.bodega.models import Bodega
from core.representantetecnico.forms.formBodega import BodegaForm


class BodegaCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    permission_required = ('bodega.add_bodega',)
    model = Bodega
    form_class = BodegaForm
    template_name = "bodega/create.html"
    success_url = reverse_lazy("rp:bodegas")
    url_redirect = success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usertitle'] = "Representante Técnico"
        context['title'] = "Registro bodegas"
        context['icontitle'] = "plus"
        context['url_list'] = self.success_url
        context['action'] = 'add'
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": self.success_url, "uriname": "Bodegas"},
            {"uridj": reverse_lazy('rp:registrobodega'), "uriname": "Registro"}
        ]
        return context

    def post(self, request, *args, **kwargs):
        data = None
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data = {}
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
