from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from core.base.mixins import IsUserUCSCSF


class DashBoard(LoginRequiredMixin, IsUserUCSCSF, TemplateView):
    template_name = 'dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
