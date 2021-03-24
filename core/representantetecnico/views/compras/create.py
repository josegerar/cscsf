import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins import ValidatePermissionRequiredMixin
from core.representantetecnico.forms.formCompra import ComprasForm
from core.representantetecnico.models import ComprasPublicas, ComprasPublicasDetalle, EstadoTransaccion


class ComprasCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    # appname.action(add, change, delete, view)_table
    permission_required = (
        'representantetecnico.add_compraspublicas',
        'representantetecnico.add_compraspublicasdetalle',
    )
    model = ComprasPublicas
    form_class = ComprasForm
    template_name = 'compras/create.html'
    success_url = reverse_lazy('rp:compras')
    url_redirect = success_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usertitle'] = "Representante Técnico"
        context['title'] = "Registrar compra"
        context['icontitle'] = "plus"
        context['url_list'] = self.success_url
        context['action'] = 'add'
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": self.success_url, "uriname": "Compras"},
            {"uridj": reverse_lazy('rp:registrocompras'), "uriname": "Registro"}
        ]
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action')
            if action == 'add':
                form = self.get_form()
                if form.is_valid():
                    compra = form.instance
                    if compra is not None:
                        with transaction.atomic():
                            sustancias = json.loads(request.POST['sustancias'])
                            estadocompra = EstadoTransaccion.objects.get(estado='registrado')
                            compra.estado_compra_id = estadocompra.id
                            compra.save()

                            for i in sustancias:
                                stock_selected = i['stock_selected']

                                det = ComprasPublicasDetalle()
                                det.stock_id = stock_selected['id']
                                det.compra_id = compra.id
                                det.cantidad = float(i['cantidad_ingreso'])
                                det.save()
                    else:
                        data['error'] = 'Ha ocurrido un error'
                else:
                    data['error'] = 'Ha ocurrido un error'
            else:
                data['error'] = 'No ha realizado ninguna accion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
