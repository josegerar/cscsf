from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from core.base.formaters import format_datetime
from core.base.mixins import ValidatePermissionRequiredMixin
from core.representantetecnico.forms.formRepositorio import RepositorioForm
from core.representantetecnico.models import Repositorio


class RepositorioListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    permission_required = ('representantetecnico.view_repositorio',)
    template_name = "repositorio/list.html"
    url_redirect = reverse_lazy('dashboard')

    def dispatch(self, request, *args, **kwargs):
        try:
            self.object = None
            pk = kwargs.get('pk')
            if pk is not None:
                self.object = Repositorio.objects.get(pk=pk)
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            messages.error(request, str(e))
        return HttpResponseRedirect(self.url_redirect)

    def get(self, request, *args, **kwargs):
        try:
            action = request.GET.get('action')
            if action is not None:
                if action == 'searchcontent':
                    type_content = request.GET.get('type')
                    data = {'data': self.get_content(type_content, request.user),
                            'urlrepository': reverse_lazy('rp:repositorio'),
                            'ruta': self.get_path_uris(self.object)}
                    return JsonResponse(data, safe=False)
        except Exception as e:
            messages.error(request, str(e))
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action')
            if action is not None:
                if action == 'newfolder':
                    nombrecarpeta = request.POST.get('nombrecarpeta')
                    self.create_folder(nombrecarpeta)
                elif action == 'createfile':
                    self.create_file(request)
                elif action == 'deleteitem':
                    self.delete_item(request)
                elif action == 'restoreitem':
                    self.restore_item(request)
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)

    def get_content(self, type_content, user):
        data = []
        if self.object is not None:
            if type_content == 'repository':
                query = Repositorio.objects.filter(user_creation_id=user.id, parent_id=self.object.id,
                                                   is_recicle_bin=False)
            elif type_content == 'recicle':
                query = Repositorio.objects.filter(user_creation_id=user.id, parent_id=self.object.id,
                                                   is_recicle_bin=True)
            else:
                query = Repositorio.objects.filter(user_creation_id=user.id, parent_id=self.object.id)
        else:
            if type_content == 'repository':
                query = Repositorio.objects.filter(user_creation_id=user.id, parent=None, is_recicle_bin=False)
            elif type_content == 'recicle':
                query = Repositorio.objects.filter(user_creation_id=user.id, parent=None, is_recicle_bin=True)
            else:
                query = Repositorio.objects.filter(user_creation_id=user.id, parent=None)
        for content in query:
            item = {'id': content.id, 'nombre': content.nombre,
                    'create_date': format_datetime(content.date_creation),
                    'url': '', 'is_file': content.is_file, 'is_dir': content.is_dir,
                    'is_recicler': content.is_recicle_bin, 'parent': 0}
            if content.is_file:
                item['url'] = content.documento.url
            if self.object is not None:
                item['parent'] = self.object.id
            data.append(item)
        return data

    def create_folder(self, nombre_carpeta):
        if nombre_carpeta is not None:
            new_folder = Repositorio()
            new_folder.nombre = nombre_carpeta
            new_folder.is_dir = True
            if self.object is not None:
                new_folder.parent_id = self.object.id
            new_folder.save()
        else:
            raise Exception('Faltan datos')

    def create_file(self, request):
        repositorio_form = RepositorioForm(request.POST, request.FILES, instance=None)
        if repositorio_form.is_valid():
            item_repositorio = repositorio_form.instance
            item_repositorio.is_file = True
            if self.object is not None:
                item_repositorio.parent_id = self.object.id
            item_repositorio.save()
        else:
            raise Exception(repositorio_form.errors)

    def delete_item(self, request):
        id_item = request.POST.get('id')
        if id_item is not None:
            with transaction.atomic():
                item_repositorio = Repositorio.objects.get(pk=id_item)
                if item_repositorio.is_recicle_bin:
                    item_repositorio.delete()
                else:
                    self.activate_all_child_recile_bin(item_repositorio)
        else:
            raise Exception('Faltan datos')

    def activate_all_child_recile_bin(self, repositorio):
        for rep in repositorio.repositorio_set.all():
            self.activate_all_child_recile_bin(rep)
        repositorio.is_recicle_bin = True
        repositorio.save()

    def restore_item(self, request):
        id_item = request.POST.get('id')
        if id_item is not None:
            with transaction.atomic():
                item_repositorio = Repositorio.objects.get(pk=id_item)
                self.restore_all_child_recile_bin(item_repositorio)
        else:
            raise Exception('Faltan datos')

    def restore_all_child_recile_bin(self, repositorio):
        for rep in repositorio.repositorio_set.all():
            self.activate_all_child_recile_bin(rep)
        repositorio.is_recicle_bin = False
        repositorio.save()

    def get_path_uris(self, repositorio):
        items = []
        while repositorio is not None:
            items.append({'id': repositorio.id, 'nombre': repositorio.nombre})
            repositorio = repositorio.parent
        return items
