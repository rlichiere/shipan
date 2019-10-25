# -*- coding: utf-8 -*-
from . import constants


def get(method_name, executor=None, request=None, obj=None):
    _executor = executor
    if not _executor:
        try:
            _executor = request.user
        except AttributeError:
            try:
                _executor = obj.executor
            except AttributeError:
                _executor = 'n.a.'

    _obj = ('%s.' % obj.__class__.__name__) if obj else ''

    _prefix = '[%s] %s%s:' % (_executor, _obj, method_name)

    return Logger(_prefix)


def setLevel(level):
    constants.django_logger.setLevel(level)


class Logger(object):

    def __init__(self, prefix=None):
        self.prefix = prefix if prefix else ''

    """ Public """

    def debug(self, *args, **kwargs):
        self._print(constants.LEVELS.DEBUG, *args, **kwargs)

    def info(self, *args, **kwargs):
        self._print(constants.LEVELS.INFO, *args, **kwargs)

    def deprecate(self, *args, **kwargs):
        self._print(constants.LEVELS.DEPRECATE, *args, **kwargs)

    def warning(self, *args, **kwargs):
        self._print(constants.LEVELS.WARNING, *args, **kwargs)

    def error(self, *args, **kwargs):
        self._print(constants.LEVELS.ERROR, *args, **kwargs)

    def exception(self, *args, **kwargs):
        self._print(constants.LEVELS.EXCEPTION, *args, **kwargs)

    def critical(self, *args, **kwargs):
        self._print(constants.LEVELS.CRITICAL, *args, **kwargs)

    def fatal(self, *args, **kwargs):
        self._print(constants.LEVELS.FATAL, *args, **kwargs)

    """ Private """

    @staticmethod
    def _buildMessage(*args, **kwargs):
        _msg = ''
        if len(args) > 0:
            _msg += args[0]
        if len(args) > 1:
            _msg += ': %s' % args[1]

        if _msg != '' and len(kwargs) > 0:
            _msg += ', '

        _msg += ', '.join([('%s: %s' % (_k, _v)) for _k, _v in kwargs.iteritems()])

        return _msg

    def _print(self, level, *args, **kwargs):
        _msg = self._buildMessage(*args, **kwargs)
        _print = constants.LEVELS.getLevelMethod(level)
        _print(' '.join([self.prefix, _msg]))
