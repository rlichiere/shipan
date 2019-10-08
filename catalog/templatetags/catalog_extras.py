# -*- coding:utf-8 -*-
from django import template

from ..models import ProductCategory

register = template.Library()


class Tag_load_categories_Node(template.Node):
   """
       This rendering Node is dedicated to the :tag:`load_categories` tag.
   """

   def __init__(self):
      pass

   def render(self, context):
      context['categories'] = ProductCategory.objects.all()
      return ''


@register.tag
def load_categories(parser, params):
   return Tag_load_categories_Node()
