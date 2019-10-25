# -*- coding: utf-8 -*-
import os
import sys
from datetime import datetime as dt

from django.contrib import messages
from django.core.management import call_command
from django.utils.safestring import mark_safe

from shipan import config

from . import utils_date


def backup_instances(model_admin, request, queryset):
    _module = queryset.model.__module__.split('.')[0]
    _modelName = '%s.%s' % (_module, queryset.model.__name__)
    _now = dt.now()
    _fileName = '%s_%s.json' % (_modelName, utils_date.format_for_file(_now))
    _filePath = '%s/%s' % (config.BACKUP_ROOT, _fileName)

    if os.path.exists(_filePath):
        _msgHtml = 'Ignored. Reason : Output file already exist (<code>%s</code>)' % _filePath
        _msgLevel = messages.ERROR
    else:
        _sysOut = sys.stdout
        sys.stdout = open(_filePath, 'w')
        call_command('dumpdata', '--indent', '2', _modelName)
        sys.stdout = _sysOut

        _count = queryset.count()
        _msg = '%s %s instance%s processed.' % (_count, _modelName, '' if _count == 1 else 's')
        _link = '<a href="/backoffice/backup/%s" target="_blank">Download backup file %s</a>' % (_fileName, _fileName)
        _msgHtml = '%s %s' % (_msg, _link)
        _msgLevel = messages.INFO

    model_admin.message_user(request, mark_safe(_msgHtml), extra_tags='safe', level=_msgLevel)
