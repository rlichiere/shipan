# -*- coding: utf-8 -*-
import os

from shipan.core.exceptions import ShipanSecurityError
import logging


class ConsoleDefaultTheme(object):
    """
    Defines the theme properties and their default values.
    """
    TitleBorderTopIcon = '_'
    TitleBorderBottomIcon = '-'
    IconError = '*'
    IconException = 'X'
    FooterBorderTopIcon = '-'
    FooterBorderBottomIcon = '_'


class ConsoleLayoutClass(object):
    """
    This static class managed the layout for the console.
    """
    def __init__(self):

        # Placement properties
        self._ScreenWidth = 160
        self._TableColumnMaxWidth = 30
        self._TableColumnsWidth = list()
        self._TableGrid = 5

        self._theme = ConsoleDefaultTheme

        self._layoutIsSynchronized = False

        self.refresh()


    def applyTheme(self, theme):
        """
        Applies a new console theme to the layout
        :param theme:
        :type theme: ConsoleDefaultTheme
        :return:
        """
        self._theme = theme


    def refresh(self):
        """
        Update layout coordinates according to configuration
        """

        # recalculate the columns width according to screenwidth
        _avgColWidth = min(self._ScreenWidth / self.get_TableGrid(), self._TableColumnMaxWidth)
        _lastColWidth =  self._ScreenWidth - _avgColWidth * (self.get_TableGrid() - 1)
        self._TableColumnsWidth = [_avgColWidth, _avgColWidth, _avgColWidth, _lastColWidth]

        self._layoutIsSynchronized = True


    def get_ScreenWidth(self):
        return self._ScreenWidth

    def get_TableGrid(self):
        return self._TableGrid

    def get_TableColumnWidth(self, column_index=None):
        return self._TableColumnsWidth[column_index]

    def get_TableColumnsWidth(self, columns_index=list()):
        _width = 0
        for _colIndex in columns_index:
            _width += self.get_TableColumnWidth(_colIndex)
        return _width

    @property
    def Theme(self):
        return self._theme

ConsoleLayout = ConsoleLayoutClass()


class SettingsLogger(object):

    _colWidths = [ConsoleLayout.get_TableColumnWidth(0), ConsoleLayout.get_TableColumnWidth(1)]

    def __init__(self, obj=None, func_name=None, loader=None):
        """
        A SettingsLogger should be instanciated:

        * in every talkative method
        * as late as possible in order avoid unnecessary code execution

        Example:
        ```
        > def some_func():
        >     L = SettingsLogger(self, 'some_func')
        >     L.debug('some message')

        Layout tools are available to facilitate the logging of settings, and their readability in a console.

        Example:
        ```
        > def some_func():
        >     L = SettingsLogger(self, 'some_func')
        >     L.print_table_title()
        >     L.print_table_bool('some_assertion', some_boolean_expression, 'shown_if_true', 'shown_if_false')
        ```

        :param obj: caller object
        :type obj: object
        :param func_name: name of the caller function
        :type func_name: str
        :param loader:
        :type loader: SettingsLoader
        """
        self._prefix = ''
        self._loader = loader
        self._isOutputReady = False
        self._buffer = list()

        # initialize with `obj class` if obj given
        if obj: self._prefix += obj.__class__.__name__

        # add a separator between class and function name if both are provided
        if obj and func_name: self._prefix += '.'

        # append with `method` if given
        if func_name: self._prefix += func_name


    """ Public """

    def print_title(self, msg):
        self.print_divider(width=ConsoleLayout.get_TableColumnsWidth([0, 1]) - 2, log_level='DEBUG')
        self._print(self._buildLineTitle(name=msg.upper(), sep=' '), log_level='DEBUG')
        self.print_divider(sep='-', width=ConsoleLayout.get_TableColumnsWidth([0, 1]) - 2, log_level='DEBUG')

    def print_footer(self, msg):
        self.print_divider(sep='-', width=ConsoleLayout.get_TableColumnsWidth([0, 1]) - 2, log_level='DEBUG')
        self._print(self._buildLineTitle(name=msg.upper(), sep=' '), log_level='DEBUG')
        self.print_divider(log_level='DEBUG')

    def print_divider(self, sep='_', width=ConsoleLayout.get_ScreenWidth(), log_level='DEBUG'):
        self._print(self._buildLineSep(sep=sep, width=width), log_level=log_level)

    def print_err(self, msg):
        self._print(self._buildLineData('ERROR', msg, sep='*'), log_level='ERROR')

    def print_exc(self, msg, exc_class):
        _msg = 'EXCEPTION: ' + msg
        _remainingWidth = ConsoleLayout.get_ScreenWidth() - ConsoleLayout.get_TableColumnsWidth([0, 1]) + 1
        self._print(self._buildLineData(exc_class.__name__, _msg.ljust(_remainingWidth, ConsoleLayout.Theme.IconError), sep='X'), log_level='ERROR')
        self._print(self._buildLineSep(), log_level='ERROR')
        self._print(self._buildLineData(exc_class.__name__, 'EXIT'), log_level='ERROR')

    def raise_exc(self, msg, exc_class):
        self.print_err(msg)
        raise exc_class(msg)

    def print_table_title(self):
        self._print(self._buildLineTitle('[ SOURCE ]', '[ NAME ]', '[ MESSAGE ]'), log_level='DEBUG')

    def print_table_bool(self, name, value, msg_ok, msg_err):
        self._print(self._buildLineData(name, (msg_ok if value else msg_err)), log_level='DEBUG')

    def print_table_ok(self, name, msg=None):
        self._print(self._buildLineData(name, msg), log_level='DEBUG')

    def print_table_warn(self, name, msg):
        self._print(self._buildLineData(name, 'WARNING: ' + msg), log_level='WARNING')

    def print_table_err(self, name, msg):
        _msg = 'ERROR: ' + msg + ' '
        _remainingWidth = ConsoleLayout.get_ScreenWidth() - ConsoleLayout.get_TableColumnsWidth([0, 1]) + 1
        self._print(self._buildLineData(name, _msg.ljust(_remainingWidth, '*'), sep='*'), log_level='ERROR')

    def print_var_exc(self, name, msg):
        _msg = 'EXCEPTION: ' + msg
        _remainingWidth = ConsoleLayout.get_ScreenWidth() - ConsoleLayout.get_TableColumnsWidth([0, 1]) + 1
        self._print(self._buildLineData(name, _msg.ljust(_remainingWidth, 'X'), sep='X'), log_level='ERROR')
        self._print(self._buildLineSep(), log_level='ERROR')
        self._print(self._buildLineData(name, 'EXIT'), log_level='ERROR')

    def raise_var_exc(self, name, msg, exc_class):
        self.print_table_err(name, msg)
        raise exc_class(msg)

    def _print(self, message, log_level, skip_buffer_check=False):

        if skip_buffer_check:
            print(message)
            return

        if self.isOutputReady:
            self._flushBuffer()

            if logging.getLevelName(log_level) >= logging.getLevelName(self._loader.LOG_LEVEL):
                print(message)
            return

        if self._buffer is not None:
            self._buffer.append({
                'LOG_LEVEL': log_level,
                'MESSAGE': message
            })


    @property
    def isOutputReady(self):
        if self._isOutputReady:
            return True

        if self._loader.LOG_LEVEL is None:
            return False

        return True


    def _flushBuffer(self):
        if self._buffer is None:
            return

        for _bufferItem in self._buffer:
            _logLevel = _bufferItem['LOG_LEVEL']
            _msg = _bufferItem['MESSAGE']

            if logging.getLevelName(_logLevel) >= logging.getLevelName(self._loader.LOG_LEVEL):
                self._print(_msg, skip_buffer_check=True, log_level=_logLevel)

        self._buffer = None
        self._isOutputReady = True


    @classmethod
    def getHigherLogLevel(cls):
        _funcGetLevelNames = getattr(logging, '_levelNames')
        _levelCodes = [_ for _ in _funcGetLevelNames.keys() if type(_) is int]
        _higherCode = max(_levelCodes)
        return _funcGetLevelNames.get(_higherCode, _funcGetLevelNames[_higherCode])



    """ Should be abstract implementations """

    def debug(self, *args, **kwargs):
        _res = 'DEBUG: '
        _res += ', '.join(list(args))
        _res += ', '.join(['%s: %s' % (_k, _v) for _k, _v in kwargs.iteritems()])
        self._print(self._buildLineData(name='', msg=_res, sep=' '), log_level='DEBUG')


    """ Private """

    def _buildLineData(self, name, msg, sep=None):
        return self._buildLine(self._prefix, name, msg, sep=sep)


    def _buildLineTitle(self, source=None, name='', msg=None, sep=' '):
        return self._buildLine(source if source else self._prefix, name, msg, sep=sep)


    def _buildLine(self, prefix, name, msg=None, sep=None):
        if not sep: sep = ' '

        _just = (prefix + ' ').ljust(self._getColumnWidth(0) - 1, sep)
        _line = '{prefix}{name} {msg}'.format(prefix=_just,
                                              name=(' ' + name if name else '').rjust(self._getColumnWidth(1) - 1, sep),
                                              msg=(msg if msg else ''))
        return _line


    @classmethod
    def _buildLineSep(cls, sep='_', width=ConsoleLayout.get_ScreenWidth()):
        return ''.join(sep for _ in range(width))


    def _getColumnWidth(self, column_index):
        """
        Return the configured width (in chars) for the given column index.

        If the given column index exceeds the number of configured columns, the width of the last column is returned.

        :param column_index: index of the column for which to retrieve the width
        :param column_index: int
        :return: the width (in chars) for the given column
        :rtype: int
        """
        return self._colWidths[column_index if column_index <= len(self._colWidths) else -1]


class SettingsLoader(object):

    def __init__(self, prefix, default_secret_key, force_security=False):
        self._prefix = prefix
        self._envDebug = None
        self._defaultSecretKey = default_secret_key
        self._envSecretKey = None
        self._envLogLevel = None
        self._envLogServices = None
        self._forceSecurity = force_security


    def parse(self, environ):
        """
        Parse given environment variables and store their values.

        :param environ: object returned by `os.environ`
        :type environ: instance
        """
        L = SettingsLogger(self, 'parse', loader=self)
        L.print_title('parse...')
        L.print_table_title()


        # DEBUG
        self._envDebug = environ.get('DEBUG', False)
        L.print_table_bool('DEBUG', self._envDebug, 'is set', 'is not set')
        L.debug('os.environ has %s keys' % len(environ))


        # LOG_LEVEL
        _logLevel = environ.get('LOG_LEVEL')
        if _logLevel:
            L.print_table_ok('LOG_LEVEL', 'use environment level : %s' % _logLevel)
        else:
            _logLevel = 'DEBUG' # removed 'INFO'
            L.print_table_ok('LOG_LEVEL', 'use default level : %s' % _logLevel)
        self._envLogLevel = _logLevel

        # LOG_SERVICES
        _AVAILABLE_LOG_SERVICES = ['SERVER', 'SQL', 'SHIPAN']
        _logServices = os.environ.get('LOG_SERVICES')
        if _logServices:
            _logServices = _logServices.split(',')
            L.debug(received_services='received %s service%s : %s' % (len(_logServices),
                                                                      ('s' if len(_logServices) > 1 else ''),
                                                                      (', '.join(_logServices))))
            if '*' in _logServices:
                _logServices = _AVAILABLE_LOG_SERVICES
                L.print_table_ok('LOG_SERVICES', 'use all services : %s' % (', '.join(_logServices)))
        else:
            _logServices = ['SHIPAN']
            L.print_table_ok('LOG_SERVICES', 'use default services : %s' % (', '.join(_logServices)))
        self._envLogServices = _logServices


        # SECRET_KEY
        _secretKey = os.environ.get('SECRET_KEY', None)
        if not _secretKey:

            if not self.DEBUG:
                _msg = 'The SECRET_KEY used for production must be passed dynamically!'
                if not self._forceSecurity:
                    # L.print_var_exc('SECRET_KEY', _msg, ShipanSecurityError)
                    L.raise_var_exc('SECRET_KEY', _msg, ShipanSecurityError)
                    # raise ShipanSecurityError(_msg)
                L.print_table_warn('SECRET_KEY', _msg)

            _secretKey = self._defaultSecretKey
            L.print_table_ok('SECRET_KEY', 'use default key (reserved to DEBUG mode): %s' % self._getShortenDefaultKey(_secretKey))
        else:
            L.print_table_ok('SECRET_KEY', 'use environment key (PROD mode) : %s' % self._getShortenSecretKey(_secretKey))

        self._envSecretKey = _secretKey

        L.print_footer('Parsed successfully')


    @property
    def DEBUG(self):
        return self._envDebug

    @property
    def SECRET_KEY(self):
        return self._envSecretKey

    @property
    def LOG_LEVEL(self):
        return self._envLogLevel

    @property
    def LOG_SERVICES(self):
        return self._envLogServices


    """ Private """

    @staticmethod
    def _getShortenDefaultKey(msg):
        return msg[:13] + '...'

    @staticmethod
    def _getShortenSecretKey(msg):
        return msg[:3] + '..........' + msg[-3:]
