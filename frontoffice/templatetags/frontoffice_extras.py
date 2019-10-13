# -*- coding: utf-8 -*-
from django import template

from ..models import DynamicPage


register = template.Library()


class Tag_get_flow_links_Node(template.Node):

   def __init__(self, flow_name, context_var):
      self.flow_name = flow_name
      self.context_var = context_var

   def render(self, context):
      context[self.context_var] = DynamicPage.objects.filter(flow=self.flow_name).values('name', 'title')
      return ''


@register.tag
def get_flow_links(parser, params):
   _bits = params.split_contents()

   _flowName = _bits[1]
   _contextVar = _bits[3]
   return Tag_get_flow_links_Node(_flowName, _contextVar)
