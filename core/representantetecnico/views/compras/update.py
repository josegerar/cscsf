import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.contrib import messages

from app.settings import LOGIN_REDIRECT_URL
from core.base.mixins import ValidatePermissionRequiredMixin
from core.representantetecnico.forms.formCompra import ComprasForm
from core.representantetecnico.models import ComprasPublicas, ComprasPublicasDetalle, EstadoTransaccion


class ComprasUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    permission_required = ('representantetecnico.change_compraspublicas',)
    model = ComprasPublicas
    form_class = ComprasForm
    template_name = 'compras/create.html'
    success_url = reverse_lazy('rp:compras')
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object is not None:
            if self.object.estado_compra is not None:
                if self.object.estado_compra.estado == 'almacenado':
                    messages.error(request, 'Registro de compra ya almacenado en bodega')
                    messages.error(request, 'No es posible su modificación')
                    messages.error(request, 'Pongase en contacto con el administrador del sistema')
                    return HttpResponseRedirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usertitle'] = "Representante Técnico"
        context['title'] = "Actualizar compra"
        context['icontitle'] = "edit"
        context['url_list'] = self.success_url
        context['action'] = 'edit'
        context['urls'] = [
            {"uridj": LOGIN_REDIRECT_URL, "uriname": "Home"},
            {"uridj": self.success_url, "uriname": "Compras"},
            {"uridj": reverse_lazy('rp:registrocompras'), "uriname": "Edicción"}
        ]
        return context

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action')
            if action is not None:
                if action == 'edit':
                    form = self.get_form()
                    if form.is_valid():
                        compra = form.instance
                        estadocompra = EstadoTransaccion.objects.get(estado='registrado')
                        if compra is not None and estadocompra is not None:
                            with transaction.atomic():
                                detalle_compras_new = json.loads(request.POST['detalle_compra'])
                                compra.estado_compra_id = estadocompra.id
                                compra.save()
                                detalle_compras_old = ComprasPublicasDetalle.objects.filter(compra_id=compra.id)

                                for dc_old in detalle_compras_old:
                                    exits_old = False
                                    for dc_new in detalle_compras_new:
                                        if dc_old.id == dc_new['id']:
                                            exits_old = True
                                    if exits_old is False:
                                        dc_old.delete()

                                detalle_compras_old = ComprasPublicasDetalle.objects.filter(compra_id=compra.id)

                                for dc_new in detalle_compras_new:
                                    exits_old = False
                                    item_det_new = None
                                    stock_old = dc_new['stock']
                                    sustancia_new = stock_old['sustancia']
                                    stock_selected = sustancia_new['stock_selected']

                                    for dc_old in detalle_compras_old:
                                        if dc_old.id == dc_new['id']:
                                            exits_old = True
                                            item_det_new = dc_old

                                    if exits_old is False and item_det_new is None:
                                        item_det_new = ComprasPublicasDetalle()

                                    item_det_new.stock_id = stock_selected['id']
                                    item_det_new.compra_id = compra.id
                                    item_det_new.cantidad = float(dc_new['cantidad_ingreso'])
                                    item_det_new.save()
                        else:
                            data['error'] = 'ha ocurrido un error'
                    else:
                        data['error'] = 'ha ocurrido un error'

                elif action == 'searchdetail':
                    data = []
                    detalle_compras = ComprasPublicasDetalle.objects.filter(compra_id=self.object.id)
                    for dci in detalle_compras:
                        data.append(dci.toJSON(rel_compraspublicas=True))
                else:
                    data['error'] = 'ha ocurrido un error'
            else:
                data['error'] = 'ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
