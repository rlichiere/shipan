# -*- coding: utf-8 -*-
import argparse
from datetime import datetime as dt
from datetime import time, timedelta
import math
import os
import random
import re
import sys
import traceback

import json

from django.contrib.auth.models import ContentType, Group, Permission, PermissionDenied, User
from django.db.models.base import ModelBase
from django.shortcuts import get_object_or_404, HttpResponse, HttpResponseRedirect, Http404, redirect, render, reverse
from django.views.generic import View, TemplateView

from shipan import settings, config, const

from . import constants
from . import logger
from . import utils_date, utils_price, utils_version, utils_exception as exc

from people.models.client import Client
from people.models.address import Address

from catalog.models import ProductCategory
from catalog.models import ProductColor
from catalog.models import ProductColouring
from catalog.models import ProductMainColor
from catalog.models import ProductModel
from catalog.models import ProductSelection
from catalog.models import ProductSize


class Tool(object):

   main_module = sys.modules[__name__]
   tools = dict()
   configurationProperties = list()
   configurationPrefix = '_ToolsConf__'


   """ PRIVATE """

   _raisableModels = list()

   """ Storage methods """

   @classmethod
   def _define(cls, name, value):
      _old = cls.tools.get(name)
      setattr(cls.main_module, name, value)
      cls.tools[name] = value
      return _old

   @classmethod
   def _undefine(cls, name):
      _old = cls.tools.get(name)
      delattr(cls.main_module, name)
      return _old

   @classmethod
   def getConfigurationRadical(cls, configuration_key):
      _prefix = cls.configurationPrefix
      _foundAt = configuration_key.find(_prefix)
      if _foundAt != 0:
         raise Exception('Configuration prefix not found for property %s' % configuration_key)
      return configuration_key[len(_prefix):]

   @classmethod
   def _getConfigurationKey(cls, name):
      return '%s%s' % (cls.configurationPrefix, name)


   """ PUBLIC """

   @classmethod
   def addRaisableModel(cls, model):
      # append model if not already stored
      try:
         cls._raisableModels.index(model)
      except ValueError:
         cls._raisableModels.append(model)

   @classmethod
   def getRaisableModels(cls):
      return cls._raisableModels

   @classmethod
   def setRaisableModels(cls, models):
      for _model in models:
         # append _model if not already stored
         try:
            cls._raisableModels.index(_model)
         except ValueError:
            cls._raisableModels.append(_model)

   @classmethod
   def set(cls, **kwargs):
      _olds = dict()
      for _name, _value in kwargs.iteritems():
         # store name and value
         _olds[_name] = cls._define(_name, _value)

      if len(kwargs) > 1:
         return _olds
      return _olds[kwargs.keys()[0]]

   @classmethod
   def add(cls, **kwargs):
      cls.set(**kwargs)

   @classmethod
   def list(cls):
      return cls.tools

   @classmethod
   def get(cls, name, default=None):
      """
      Returns the value of the tool corresponding to given name.

      :param name: name of the tool to retrieve
      :type name: str
      :param default: value to return if the tool corresponding to the given name does not exist
      :type default: None, object
      :return: the value of the tool
      :rtype: object, iterable

      Examples:

      ```
      > # Retrieve the value of the `s` tool
      > Tool.get('s')
      'abc'

      > # Retrieve the value of the `User` tool
      > Tool.get('User')
      <class 'django.contrib.auth.models.User'>

      > # Retrieve the value of the `u` tool
      > Tool.get('u')
      <User: admin>

      > # Retrieve an inexistent tool
      > Tool.get('1n3x1st3nt_tOOl', 'd3f4ult_v4lu3')
      'd3f4ult_v4lu3'
      ```
      """
      try:
         return getattr(cls.main_module, name)
      except AttributeError:
         return default

   @classmethod
   def pop(cls, name):
      _old = cls.get(name)
      cls._undefine(name)
      return _old


   """ Formatters """

   @classmethod
   def as_dict(cls, variable, value_module, value_class, value):
      _data = {
         'variable': variable,
         'value_module': value_module,
         'value_class': value_class,
         'value': value,
      }
      if hasattr(value, 'id'):
         _data['value_id'] = value.id
      if hasattr(value, 'pk'):
         _data['value_pk'] = value.pk

      return _data

   """ Management Logic """

   @classmethod
   def buildToolsData(cls):
      _toolsData = list()
      for _toolName, _toolValue in cls.list().iteritems():
         _toolType = type(_toolValue)

         # manage Tool configuration property case
         if _toolName in cls.configurationProperties:
            _toolValueModule = cls.__module__
            _toolValueClass = cls.__name__

            _toolsData.append(cls.as_dict(_toolName, _toolValueModule, _toolValueClass, _toolValue))
            continue

         # manage Tool data property case
         if _toolType is ModelBase:
            # manage Model instance case
            _toolValueModule = _toolValue.__module__[:_toolValue.__module__.rfind('.')]
            _toolValueClass = _toolValue.__module__[_toolValue.__module__.rfind('.') + 1:]
            _toolValue = _toolValue.__name__

         elif hasattr(_toolType, '__base__') and _toolType.__base__ is object:
            # manage object subclasses case
            _toolValueModule = _toolType.__module__
            _toolValueClass = _toolType.__name__
            if _toolType.__name__ == 'module':
               # tool value is an imported module
               _toolValue = _toolValue.__name__
            elif _toolType.__name__ == 'type':
               # tool value is a class implementation
               _toolValue = '%s.%s' % (_toolValue.__module__, _toolValue.__name__)
            else:
               # dont't change _toolValue
               pass

         else:
            # manage simple cases, such as bool, int, str, etc
            _toolValueModule = _toolType.__module__
            _toolValueClass = _toolType.__name__

         _toolsData.append(cls.as_dict(_toolName, _toolValueModule, _toolValueClass, _toolValue))

      return _toolsData

   @classmethod
   def calculateColumnsWidth(cls, data):
      return {
         'variable': max([len(cls.getConfigurationRadical(_['variable'])
                              if _['variable'] in cls.configurationProperties else _['variable'])
                          for _ in data]),
         'value_module': max([len(_['value_module']) for _ in data]),
         'value_class': max([len(_['value_class']) for _ in data]),
         'value': max([len(ToolPrinter.get_printable(_['value'])) for _ in data]),
         'value_id': max([len(str(_['value_id'])) for _ in data if 'value_id' in _]),
         'value_pk': max([len(str(_['value_pk'])) for _ in data if 'value_pk' in _]),
      }

   """ Tool configurations methods """

   @classmethod
   def getConfiguration(cls, name):
      _name = cls._getConfigurationKey(name)
      if _name not in cls.configurationProperties:
         raise Exception('Configuration property %s not found in %s' % (name, cls.configurationProperties))
      return getattr(cls.main_module, _name)

   @classmethod
   def configure(cls, **kwargs):
      _olds = dict()
      for _name, _value in kwargs.iteritems():
         _newName = cls._getConfigurationKey(_name)
         _olds[_name] = cls._define(_newName, _value)
         cls.configurationProperties.append(_newName)

      if len(kwargs) > 1:
         return _olds
      return _olds[kwargs.keys()[0]]

   @classmethod
   def unconfigure(cls, name):
      _old = cls._undefine(cls._getConfigurationKey(name))
      cls.configurationProperties.pop(name)
      return _old

   @classmethod
   def isConfiguration(cls, data):
      if data.get('variable', '') in cls.configurationProperties:
         return True
      return False


class ToolPrinter(object):

   @classmethod
   def get_printable(cls, value):
      _value = str(value)
      _toolMaxValueLen = Tool.getConfiguration('max_tool_value_len')
      if len(_value) > _toolMaxValueLen:
         return '%s ...' % _value[:_toolMaxValueLen - 4]

      return _value

   @classmethod
   def get_subliner(cls, length, char='-'):
      return ''.join([char for _ in range(0, length)])

   @classmethod
   def format(cls, data, columns_widths, line_template):
      _variable = data.get('variable')
      _value_module = data.get('value_module')
      _value_class = data.get('value_class')
      _value = ToolPrinter.get_printable(data.get('value'))
      _value_id = str(data.get('value_id', ''))
      _value_pk = str(data.get('value_pk', ''))

      _variable_width = columns_widths.get('variable', 0)
      _value_module_width = columns_widths.get('value_module', 0)
      _value_class_width = columns_widths.get('value_class', 0)
      _value_width = columns_widths.get('value', 0)
      _value_id_width = columns_widths.get('value_id', 0)
      _value_pk_width = columns_widths.get('value_pk', 0)

      return line_template.format(variable=_variable.ljust(_variable_width),
                                  value_module=_value_module.ljust(_value_module_width),
                                  value_class=_value_class.ljust(_value_class_width),
                                  value=_value.ljust(_value_width),
                                  value_id=_value_id.ljust(_value_id_width),
                                  value_pk=_value_pk.ljust(_value_pk_width))

   @classmethod
   def print_data(cls, data, colums_width, header_template, line_template):

      # build divider according to columns widths
      _divider = header_template.format(variable=cls.get_subliner(colums_width['variable']),
                                        value_module=cls.get_subliner(colums_width['value_module']),
                                        value_class=cls.get_subliner(colums_width['value_class']),
                                        value=cls.get_subliner(colums_width['value']),
                                        value_id=cls.get_subliner(colums_width['value_id']),
                                        value_pk=cls.get_subliner(colums_width['value_pk']))

      # print column names
      print(cls.format(columns_widths=colums_width,
                       line_template=header_template,
                       data={
                          'variable': 'VARIABLE',
                          'value_module': 'MODULE',
                          'value_class': 'CLASS',
                          'value': 'VALUE',
                          'value_id': 'ID',
                          'value_pk': 'PK'
                       }))

      # print divider
      print(_divider)

      # print Tool data lines
      for _toolData in data:
         if Tool.isConfiguration(_toolData):
            continue

         print(cls.format(_toolData, colums_width, line_template))

      # print divider
      print(_divider)

      # print Tool configuration lines
      for _toolData in data:
         if not Tool.isConfiguration(_toolData):
            continue

         # prepare patched tool configuration data with cleaned variable name
         _toolDataPatched = dict(_toolData)
         _toolDataPatched['variable'] = Tool.getConfigurationRadical(_toolDataPatched['variable'])

         print(cls.format(_toolDataPatched, colums_width, line_template))

   @classmethod
   def echo(cls):
      # build the local work list for tools data
      _toolsData = Tool.buildToolsData()

      # build the local work dict of columns widths
      _colsWidth = Tool.calculateColumnsWidth(_toolsData)

      # sort local work data according to the desired order
      _toolsData.sort(key=lambda _: (_['value_module'], _['value_class'], _['variable']))

      # print result
      cls.print_data(data=_toolsData,
                     colums_width=_colsWidth,
                     header_template='{variable} {value_module} {value_class} {value} {value_id} {value_pk}',
                     line_template='{variable} {value_module}.{value_class} {value} {value_id} {value_pk}')


# Add imports
Tool.add(argparse=argparse,
         dt=dt,
         time=time,
         timedelta=timedelta)

# python
Tool.add(math=math,
         os=os,
         random=random,
         re=re,
         sys=sys,
         traceback=traceback)

# required modules
Tool.add(json=json)

# django
Tool.add(ContentType=ContentType,
         Group=Group,
         Permission=Permission,
         PermissionDenied=PermissionDenied,
         User=User)

# django shortcuts
Tool.add(get_object_or_404=get_object_or_404,
         HttpResponse=HttpResponse,
         HttpResponseRedirect=HttpResponseRedirect,
         Http404=Http404,
         redirect=redirect,
         render=render,
         reverse=reverse)

# django generic views
Tool.add(View=View,
         TemplateView=TemplateView)


# exc
Tool.add(exc=exc,
         constants=constants)

# settings and config
Tool.add(settings=settings,
         config=config,
         const=const)

# tool utils
Tool.add(utils_date=utils_date,
         utils_price=utils_price,
         utils_version=utils_version)

# model User
try:
   u = User.objects.first()
except User.DoesNotExist:
   print('Skip Tool: `u`')
else:
   Tool.add(u=u)

   # logger
   l = logger.get(method_name='tools.script', executor=u)
   Tool.add(logger=logger,
            l=l)


# model Client
Tool.add(Client=Client)
try:
   cli = Client.objects.first()
except Client.DoesNotExist:
   print('Skip Tool: `cli`')
else:
   Tool.add(cli=cli)


Tool.add(ProductCategory=ProductCategory)
Tool.add(ProductColor=ProductColor)
Tool.add(ProductColouring=ProductColouring)
Tool.add(ProductMainColor=ProductMainColor)
Tool.add(ProductModel=ProductModel)
Tool.add(ProductSelection=ProductSelection)
Tool.add(ProductSize=ProductSize)



# model Address
Tool.add(Address=Address)
try:
   addr = Address.objects.first()
except Address.DoesNotExist:
   print('Skip Tool: `addr`')
else:
   Tool.add(addr=addr)



# Add Tool methods
Tool.add(echo=ToolPrinter.echo)


# Add Tool configurations
Tool.configure(max_tool_value_len=120)
