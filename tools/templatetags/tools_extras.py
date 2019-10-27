# -*- coding:utf-8 -*-
from datetime import datetime as dt

from django import template
from django.utils import translation

from people.models.client import Client

from catalog.models import ProductSelection

from tools import logger, utils_exception

from shipan import config, const, settings

register = template.Library()


@register.tag(name='load_base')
def load_base(parser, params):
    """
    Define the base variables (i.e context variables required by the base template) to current context.

    Actually, we declare the following base variables because they are required by the base template:

    * ``config``: **Shipan** main configuration
    * ``const``: **Shipan** constants
    * ``executor``: the :model:`people.Client` (otherwise :model:`auth.User`) who executes this method

    Usage::

        {% load_base %}

    """
    _l = logger.get('load_base')
    _l.verbose('unused params: parser: %(parser)s, param: %(params)s' % {'parser': type(parser), 'params': type(params)})

    class _Node(template.Node):
        def __init__(self):
            pass

        def render(self, context):
            context['config'] = config
            context['const'] = const
            context['settings'] = settings

            # retrieve the user from the wsgi request
            _user = context['request'].user

            # use the user's Client instance as executor for all registered users
            try:
                if not _user.is_anonymous:
                    _user = Client.objects.get(username=_user.username)
            except Client.DoesNotExist:
                _msg = 'Client %s not found' % _user.username
                _l.error(_msg)
                raise utils_exception.LookupExc(_msg)
            context['executor'] = _user

            # retrieve visible selections
            _now = dt.now()
            _availableSelections = ProductSelection.objects.exclude(start_at__gt=_now).exclude(ends_at__lt=_now)
            context['selection_news'] = _availableSelections.filter(kind='NEW')
            context['selection_seasons'] = _availableSelections.filter(kind='SEASON')
            return ''

    return _Node()


@register.filter(name='at')
def at_filter(data, key):
    try:
        return data[key]
    except KeyError:
        try:
            return data[translation.get_language_info(translation.get_language())['code']]
        except:
            pass
        pass
    except TypeError:
        return None


@register.tag(name='trans_db')
def trans_db_tag(parser, params):
    class _Node(template.Node):

        def __init__(self, obj_name, property_name):
            self._objName = obj_name
            self._objVariable = template.Variable(self._objName)
            self._propertyName = property_name
            self._obj = None

        def render(self, context):
            self._obj = self._objVariable.resolve(context)
            _locPropertyFunc = getattr(self._obj, self._propertyName)
            _value = _locPropertyFunc(context['request'])
            return _value

    _bits = params.split_contents()
    _objString = _bits[1]
    _propertyName = _bits[2]
    return _Node(obj_name=_objString, property_name=_propertyName)
