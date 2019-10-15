# -*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from tools.utils.utils_json import JsonFieldUtils


@python_2_unicode_compatible
class DynamicPage(models.Model):

   name = models.CharField(help_text="""
      Intern name of the page.
                           """,
                           max_length=200)

   loc_title = models.TextField(help_text="""
      Localized title of the page.
                                """,
                                default=JsonFieldUtils.get_initial_content())

   content = models.TextField(help_text="""
      Content of the page.
                              """,
                              default='',
                              blank=True)

   flow = models.CharField(help_text="""
      Flow in the page.
                           """,
                           choices=[('footer', 'Footer')],
                           max_length=200)

   flow_position = models.IntegerField(help_text="""
      Position in flow.
                                       """,
                                       default=1)

   class Meta:
      ordering = ['flow_position']

   def __str__(self):
      return self.title


   def getTitle(self, request=None):
      """
      Return the localized title, according to the given request language.

      :param request: request from which to retrieve the language
      :type request: WSGIRequest
      :return: the localized value
      :rtype: str
      """
      return JsonFieldUtils.get_field_value(instance=self, field='loc_title', request=request)
