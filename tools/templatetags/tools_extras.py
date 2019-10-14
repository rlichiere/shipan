# -*- coding:utf-8 -*-
from django import template

from people.models.client import Client

from shipan import config, const


register = template.Library()


class Tag_load_base_Node(template.Node):
   """
   This rendering Node is dedicated to the :tag:`load_base` tag.
   """
   def __init__(self):
      pass

   def render(self, context):

      # define `config` var
      context['config'] = config

      # define `const` var
      context['const'] = const

      # define `executor` var
      try:
         if not context['executor'].is_anonymous:
            context['executor'] = Client.objects.get(username=context['executor'].username)
      except KeyError:
         # manage views that do not rewrite request.user as executor
         try:
            if not context['user'].is_anonymous:
               context['executor'] = Client.objects.get(username=context['user'].username)
         except KeyError:
            if not context['request'].user.is_anonymous:
               context['executor'] = Client.objects.get(username=context['request'].user.username)
      return ''


@register.tag
def load_base(parser, params):
   return Tag_load_base_Node()
