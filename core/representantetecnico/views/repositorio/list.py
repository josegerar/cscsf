from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView

from core.representantetecnico.models import Repositorio


class RepositorioListView(ListView):
    model = Repositorio
    template_name = "repositorio/list.html"

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = None
            pk = None
            rp = Repositorio()
            if 'action' in request.POST:
                action = request.POST['action']
            if 'pk' in kwargs:
                pk = kwargs['pk']
            if action == 'newfolder':
                rp.create_folder(request.POST['nombrecarpeta'], pk)
            elif action == 'newfile':
                rp.create_file(request.FILES['file'], pk)
            data = rp.get_content_folder(pk)
            data['urlrepository'] = reverse_lazy('rp:repositorio')
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)