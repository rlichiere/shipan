# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import HttpResponse, redirect, reverse
from django.views.generic import TemplateView, View

from shipan import config

from tools import logger

from people.models.client import Client


class Home(LoginRequiredMixin, TemplateView):

    template_name = 'backoffice/home.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)

        _clients = Client.objects.all()
        _clients = _clients[max(0, _clients.count() - 5):]
        context['last_n_clients'] = _clients

        return context


class Backup(View):

    def get(self, request, **kwargs):
        _l = logger.get('get', request=request, obj=self)
        if not request.user.is_superuser:
            return redirect(reverse('fo-home'))

        _fileName = kwargs['filename']
        _filePath = '%s/%s' % (config.BACKUP_ROOT, _fileName)
        try:
            with open(_filePath, 'r') as _file:
                _fileContent = _file.read()
                return HttpResponse(_fileContent, content_type='application/json')
        except IOError:
            _l.error('Error while opening file : %s' % _filePath)
            raise Http404
