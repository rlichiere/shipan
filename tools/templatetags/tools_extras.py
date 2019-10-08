# -*- coding:utf-8 -*-
from django import template

from shipan import config

register = template.Library()


class Tag_load_config_Node(template.Node):
   """
       This rendering Node is dedicated to the :tag:`load_config` tag.
   """

   def __init__(self):
      pass

   def render(self, context):
      context['config'] = config
      return ''


@register.tag
def load_config(parser, params):
   return Tag_load_config_Node()
