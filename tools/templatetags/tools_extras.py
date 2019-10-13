# -*- coding:utf-8 -*-
from django import template

from people.models.client import Client

from shipan import config, const

register = template.Library()


class Tag_load_config_Node(template.Node):
   """
       This rendering Node is dedicated to the :tag:`load_config` tag.
   """

   def __init__(self):
      pass

   def render(self, context):

      context['config'] = config
      context['const'] = const
      if not context['user'].is_anonymous:
         context['executor'] = Client.objects.get(username=context['user'].username)
      return ''


@register.tag
def load_config(parser, params):
   return Tag_load_config_Node()
