from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from core.base.mixins import IsUserUCSCSF


class DashBoard(LoginRequiredMixin, IsUserUCSCSF, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Dashboard"
        return context

