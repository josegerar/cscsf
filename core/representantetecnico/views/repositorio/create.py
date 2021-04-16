from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView

from core.base.mixins import ValidatePermissionRequiredMixin
from core.representantetecnico.forms.formRepositorio import RepositorioForm
from core.representantetecnico.models import Repositorio


class RepositorioCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    permission_required = ('representantetecnico.add_repositorio',)
    model = Repositorio
    form_class = RepositorioForm
    template_name = "repositorio/create.html"
    success_url = reverse_lazy("rp:repositorio")
    url_redirect = success_url

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                if form.is_valid():
                    type_item = request.POST['type']
                    if type_item is None:
                        raise Exception('Faltan datos')
                    item_repositorio = form.instance
                    if type_item == 'file':
                        item_repositorio.is_file = True

                else:
                    data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)