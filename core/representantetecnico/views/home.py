from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "homerp.html"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['urls'] = [
            {"uridj": reverse_lazy('rp:index'), "uriname": "Home"}
        ]
        context['usertitle'] = "Representante Técnico"
        context['title'] = "Home"
        return context
