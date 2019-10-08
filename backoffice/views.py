# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from people.models.client import Client


class Home(LoginRequiredMixin, TemplateView):

   template_name = 'backoffice/home.html'

   def get_context_data(self, **kwargs):
      context = super(Home, self).get_context_data(**kwargs)

      _clients = Client.objects.all()
      _clients = _clients[max(0, _clients.count() - 5):]
      context['last_n_clients'] = _clients

      context['executor'] = self.request.user

      return context
