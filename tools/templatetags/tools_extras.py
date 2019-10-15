# -*- coding:utf-8 -*-
from django import template

from people.models.client import Client

from tools import logger, utils_exception

from shipan import config, const


register = template.Library()


@register.tag(name='load_base')
def load_base(parser, params):
   """
   Define the base variables (i.e context variables required by the base template) to current context.

   Actually, we declare the following base variables because they are required by the base template:

   * ``config``: **Shipan** main configuration
   * ``const``: **Shipan** constants
   * ``executor``: the :model:`people.Client` (otherwise :model:`auth.User`) who executes this method

   Usage::

      {% load_base %}

   """
   _l = logger.get('load_base')
   _l.debug('unused params: parser: %(parser)s, param: %(params)s' % {'parser': type(parser), 'params': type(params)})

   class _Node(template.Node):
      def __init__(self):
         pass

      def render(self, context):
         context['config'] = config
         context['const'] = const

         # retrieve the user from the wsgi request
         _user = context['request'].user

         # use the user's Client instance as executor for all registered users
         try:
            if not _user.is_anonymous:
               _user = Client.objects.get(username=_user.username)
         except Client.DoesNotExist:
            _msg = 'Client %s not found' % _user.username
            _l.error(_msg)
            raise utils_exception.LookupExc(_msg)
         context['executor'] = _user

         return ''

   return _Node()
