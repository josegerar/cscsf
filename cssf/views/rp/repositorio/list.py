from django.http import JsonResponse
from django.views.generic import ListView

from cssf.models import Repositorio


class RepositorioListView(ListView):
    model = Repositorio
    template_name = "rp/repositorio/list.html"

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
                print(request.POST)
                print(request.FILES)
            data = []
            obj = rp.get_content_folder(pk)
            for i in obj:
                data.append(i.toJSON())
        except Exception as e:
            data["error"] = str(e)
        return JsonResponse(data, safe=False)