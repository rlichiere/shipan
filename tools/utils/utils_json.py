# -*- coding: utf-8 -*-
import json

from django.utils import translation

from shipan import settings

from .. import logger
from . import utils_exception


class JsonFieldUtils(object):

   @staticmethod
   def get_initial_content():
      """
      Return the default content field with which to initialize the field value.

      :return:
      :rtype: str
      """
      return json.dumps({_lc[0]: "Default content for %(lang)s" % {'lang': _lc[1]} for _lc in settings.LANGUAGES})

   @classmethod
   def get_field_value(cls, instance, field, request=None):
      """
      Return the localized value of given field, according to the given request language.

      :param instance: the instance from which to retrieve the given field value
      :type instance: Model
      :param field: name of field from which to retrieve the localized field value
      :type field: str
      :param request: request
      :type request: WSGIRequest
      :return: the localized field value
      :rtype: str
      """
      _fieldData = cls.get_field_data(instance, field=field, request=request)

      if request is not None:
         return _fieldData.get(request.LANGUAGE_CODE, cls.get_default_content(instance, field=field, data=_fieldData))

      return cls.get_default_content(instance, field=field, data=_fieldData)

   @classmethod
   def get_field_data(cls, instance, field, request=None):
      """
      Return the data of the given field instance, as a valid dictionary.

      :param instance: the instance from which to retrieve the field data
      :type instance: Model
      :param field: name of field from which to retrieve the JSON data
      :type field: str
      :param request: request
      :type request: WSGIRequest
      :return: the data from the `.loc_{{field}}` instance field
      :rtype: dict
      """
      _l = logger.get('get_field_data', request=request, obj=cls)
      try:
         return json.loads(getattr(instance, field))

      except ValueError as e:
         _errLabel = 'Error while loading JSON value : %s' % utils_exception.labelize(e)
         _l.error(_errLabel)
         return {}
      except AttributeError:
         _errLabel = 'Field `%s` not found' % field
         _l.error(_errLabel)
         return {}

   @classmethod
   def get_default_content(cls, instance, field, data=None):
      """
      Return the default value for the given field.

      Elect the value corresponding to the default language (i.e `settings.LANGUAGE_CODE`) if found in field data,
       otherwise elect field `.name`.

      :param instance: the instance from which to retrieve the field default value
      :type instance: Model
      :param field: name of field from which to retrieve the JSON data
      :type field: str
      :param data:
      :type data: dict
      :return:
      :rtype: str
      """
      _data = data if data else cls.get_field_data(instance, field=field)

      if _data.has_key(settings.LANGUAGE_CODE):
         return _data[settings.LANGUAGE_CODE]

      _langInfo = translation.get_language_info(settings.LANGUAGE_CODE)
      if _data.has_key(_langInfo['code']):
         return _data[_langInfo['code']]

      return instance.name

   @classmethod
   def field_is_valid(cls, instance, field_name):
      try:
         json.JSONDecoder().decode(getattr(instance, field_name))
         return True
      except ValueError:
         return False
