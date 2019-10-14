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
      context['config'] = config
      context['const'] = const
      try:
         if not context['executor'].is_anonymous:
            context['executor'] = Client.objects.get(username=context['executor'].username)
      except KeyError:
         # manage views that do not rewrite request.user as executor
         if not context['user'].is_anonymous:
            context['executor'] = Client.objects.get(username=context['user'].username)
      return ''


@register.tag
def load_base(parser, params):
   return Tag_load_base_Node()
