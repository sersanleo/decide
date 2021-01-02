import json
from django.views.generic import TemplateView
from django.conf import settings
from django.http import Http404

from base import mods

# TODO: check permissions and census
class IndexView(TemplateView):
    template_name = 'decide/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

# TODO: check permissions and census
class LoginView(TemplateView):
    template_name = 'decide/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

# TODO: check permissions and census
class LogoutView(TemplateView):
    template_name = 'decide/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context