# -*- coding: utf-8 -*-
import json

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from shipan import settings

from tools import logger


@python_2_unicode_compatible
class DynamicPage(models.Model):

   name = models.CharField(help_text="""
      Intern name of the page.
                           """,
                           max_length=200)

   loc_title = models.CharField(help_text="""
      Localized title of the page.
                                """,
                                default='{}',
                                max_length=200)

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


   def getTitleLocalized(self, request=None):
      """
      Return the title localized according to given request language.

      :param request: request from which to retrieve the language
      :type request: WSGIRequest
      :return: the localized value
      :rtype: str
      """
      _fieldData = self.getTitleLocalizationData(request=request)

      if request is not None:
         return _fieldData.get(request.LANGUAGE_CODE, self.getTitleDefault(data=_fieldData))
      return self.getTitleDefault(data=_fieldData)

   def getTitleDefault(self, data=None):
      _data = data if data else self.getTitleLocalizationData()
      return _data.get(settings.LANGUAGE_CODE, self.name)

   def getTitleLocalizationData(self, request=None):
      _l = logger.get('getTitleLocalizationData', request=request, obj=self)
      try:
         return json.loads(self.loc_title)

      except ValueError:
         _errLabel = 'Error while load JSON value'
         _l.error(_errLabel)
         return {}

   @property
   def title(self):
      _l = logger.get('title', obj=self)
      _l.deprecate('Should be replaced by `.getTitleLocalized()`')
      return self.getTitleLocalized()
